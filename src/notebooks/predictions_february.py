import elapid
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from sklearn.metrics import make_scorer, roc_auc_score
import os
import time

# Load the data
annotation = 'src/data/annotated_1.csv'
df = pd.read_csv(annotation)

# count the number of records per year
print(df['year'].value_counts())

# Train-test split.
train_val_df = df[df['year'] < 2018]
test_df = df[df['year'] == 2018]

# Separar características (X) y objetivo (y)
cols_to_drop = ['class', 'month', 'year', 'geometry', 'longitude', 'latitude']
X_train_val = train_val_df.drop(columns=cols_to_drop)
y_train_val = train_val_df['class']

X_test = test_df.drop(columns=cols_to_drop)
y_test = test_df['class']

# Dividir el conjunto de entrenamiento en entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42)

# Crear el val_index para PredefinedSplit
val_fold = np.zeros(len(y_train) + len(y_val))
val_fold[len(y_train):] = -1  # -1 indica las muestras del conjunto de validación

# Crear el objeto PredefinedSplit
ps = PredefinedSplit(test_fold=val_fold)

# Dividir en conjunto de entrenamiento (2014-2016) y validación (2017)
#train_df = train_val_df[train_val_df['year'] < 2017]
#val_df = train_val_df[train_val_df['year'] == 2017]

# Definir el modelo base
model = elapid.MaxentModel(
    transform='cloglog',
    feature_types=['linear', 'hinge', 'product'],
    tau=0.5,
    clamp=True,
    scorer='roc_auc',
    beta_multiplier=1.5,
    beta_lqp=1.0,
    beta_hinge=1.0,
    beta_threshold=1.0,
    n_hinge_features=10,
    n_threshold_features=10,
    convergence_tolerance=1e-07,
    use_lambdas='best',
    n_cpus=4
)
# Definir el espacio de hiperparámetros para el grid search
param_grid = {
    'beta_multiplier': [1.0, 2.0],  # Valores a probar para el escalador de regularización
    'beta_lqp': [0.5, 1.5],  # Valores a probar para la regularización de características lineales, cuadráticas y de producto
    'beta_hinge': [0.5, 1.5],  # Valores a probar para la regularización hinge
    'beta_threshold': [0.5, 1.5],  # Valores a probar para la regularización umbral
    'n_hinge_features': [5, 15],  # Número de características hinge a probar
    'n_threshold_features': [5, 15],  # Número de características umbral a probar
    'clamp': [True, False],  # Probar si se debe o no clamping
    'convergence_tolerance': [1e-06, 1e-08],  # Umbrales de convergencia a probar
}
# Definir el evaluador
scorer = make_scorer(roc_auc_score, response_method='predict_proba')

# Configurar el Grid Search con validación cruzada
grid_search = GridSearchCV(model, param_grid, scoring=scorer, cv=ps, n_jobs=-1, verbose=2)

# Ejecutar el Grid Search
grid_search.fit(np.vstack([X_train, X_val]), np.hstack([y_train, y_val]))

# Resultados
print("Best parameters found: ", grid_search.best_params_)
print("Best AUC score: ", grid_search.best_score_)

# Acceso a los resultados detallados
results = grid_search.cv_results_
print("Detailed results: ")

for i in range(len(results['params'])):
    print(f"Parameters: {results['params'][i]} - Mean AUC: {results['mean_test_score'][i]:.4f} - Std AUC: {results['std_test_score'][i]:.4f}")

# Evaluar el mejor modelo en el conjunto de prueba
best_model = grid_search.best_estimator_
test_predictions = best_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, test_predictions)
print("Test AUC score: ", test_auc)
import elapid
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os
import time

# Load the data
annotation = 'src/data/annotated_2.csv'
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
#X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42)

# Dividir en conjunto de entrenamiento (2014-2016) y validación (2017)
train_df = train_val_df[train_val_df['year'] < 2017]
val_df = train_val_df[train_val_df['year'] == 2017]

# Separar características (X) y objetivo (y) para entrenamiento y validación
X_train = train_df.drop(columns=cols_to_drop)
y_train = train_df['class']

X_val = val_df.drop(columns=cols_to_drop)
y_val = val_df['class']

# Crear el modelo
model = elapid.MaxentModel(transform='cloglog', beta_multiplier=2.0)

# Medir el tiempo de entrenamiento
start_time = time.time()
print('Start training the model at:', start_time)

# Entrenar el modelo
model.fit(X_train, y_train)

# Medir el tiempo de entrenamiento
end_time = time.time()
training_duration = end_time - start_time
print(f'Tiempo de entrenamiento: {training_duration:.2f} segundos')

# Validar el modelo
y_val_pred = model.predict(X_val)
val_accuracy = metrics.roc_auc_score(y_val, y_val_pred)
print(f'Validation AUC: {val_accuracy:.3f}')

os.makedirs('src/models', exist_ok=True)
elapid.save_object(model, 'src/models/maxent_model_febrero.pkl')

# Evaluar el modelo en el conjunto de prueba
y_test_pred = model.predict(X_test)
test_accuracy = metrics.roc_auc_score(y_test, y_test_pred)
print(f'Test AUC: {test_accuracy:.3f}')

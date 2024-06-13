from database_connection import trajectories_df
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("Columnas del dataframe: \n", trajectories_df.columns)

trajectories_df["date"] = pd.to_datetime(trajectories_df["year"].astype(str) + "-" + trajectories_df["month"].astype(str))
print(trajectories_df.head())
print(trajectories_df.info())

# Barplot del número de puntos por año y por mes
sns.set(rc={'figure.figsize':(18, 10)})
ax = sns.barplot(data=trajectories_df, x="year", y="number_of_points", hue="month", palette="tab10")
ax.set_title("Cantidad de puntos de presencia por mes", fontsize=20)
ax.set_xlabel("Año", fontsize=15)
ax.set_ylabel("Cantidad de puntos", fontsize=15)
ax.legend(title="Mes", title_fontsize="15", fontsize="12")
os.makedirs("images", exist_ok=True)
plt.savefig("images/barplot_number_of_points_by_year_and_month.png")



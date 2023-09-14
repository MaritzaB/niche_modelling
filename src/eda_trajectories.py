from database_connection import trajectories_df
import pandas as pd
from pandasql import sqldf
import seaborn as sns
import matplotlib.pyplot as plt

print("Columnas del dataframe: \n", trajectories_df.columns)

## Selecciona los primeros valores de las columnas de tipo "number"
print(trajectories_df.head())
print(trajectories_df.select_dtypes("number").head())

trajectories_df["date"] = trajectories_df["date"].astype("datetime64[ns]")
#print(trajectories_df.info())
print("Dataframe description: \n", trajectories_df.describe())

## Cuenta datos de datos categóricos
print(trajectories_df.value_counts("date"))
print(trajectories_df.value_counts("name"))

plt.figure()
sns.histplot(data=trajectories_df, x="longitude", binwidth=0.5)
plt.savefig("images/histogram_longitude.png")

plt.figure()
sns.histplot(data=trajectories_df, x="latitude", binwidth=0.5)
plt.savefig("images/histogram_latitude.png")

plt.figure()
sns.boxplot(data=trajectories_df, x="longitude")
plt.savefig("images/boxplot.longitude.png")

plt.figure()
sns.boxplot(data=trajectories_df, x="latitude")
plt.savefig("images/boxplot.latitude.png")

query_dates_by_year = '''
    select
	substring(date, 1,4) as año,
	count(distinct date) as numero_fechas
    from trajectories_df
    group by substring(date, 1,4);'''
    
print(sqldf(query_dates_by_year))

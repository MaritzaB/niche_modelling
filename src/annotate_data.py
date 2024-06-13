import elapid
import pandas as pd
import geopandas as gpd
print(elapid.__version__)

trajectories = pd.read_csv('src/data/trajectories.csv')

trajectories_01 = trajectories[(trajectories['year'] == 2014) & (trajectories['month'] == 1)]
print(trajectories_01.shape)

trajectories_01.drop_duplicates(subset='geom', inplace=True)
print(trajectories_01.shape)
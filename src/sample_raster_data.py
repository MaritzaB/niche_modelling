import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import MultiPoint
import matplotlib.pyplot as plt
import rasterio

year = '2014'
month = '01'

file = 'src/data/trajectories.csv'


df = pd.read_csv(file)
geo_df = gpd.GeoDataFrame(df, geometry=df['geom'].apply(wkt.loads))
geo_df.crs = '+proj=longlat +datum=WGS84 +no_defs'

condition = (geo_df['year'] == int(year)) & (geo_df['month'] == int(month))
geom = geo_df['geometry'].where(condition).head()

s = geom.explode(index_parts=True)
s.drop_duplicates(inplace=True)

coords = [(x, y) for x, y in zip(s.x, s.y)]

sst_tiff = f'src/data/{year}/{month}/processed/{year}_{month}_jplMURSST41__sst.tif'
src = rasterio.open(sst_tiff)

values_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst'])
values_df['year'] = [year for x in coords]
values_df['month'] = str(month)
values_df['lon'] = [x for x, y in coords]
values_df['lat'] = [y for x, y in coords]
values_df['sst'] = [val[0] for val in src.sample(coords)]

# whisker plot
fig, ax = plt.subplots()
plt.boxplot(values_df['sst'])
plt.savefig(f'src/data/{year}/{month}/processed/{year}_{month}_jplMURSST41__sst_boxplot.png')

print(values_df.head())
print(values_df.dtypes)
print(values_df.describe())
print(len(values_df))

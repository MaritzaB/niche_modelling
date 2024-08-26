#!/usr/bin/env python3

#file = 'src/data/2014/01/processed/2014_01_jplMURSST41_reproj.tif'
file = 'src/data/2014/01/processed/2014_01_NESDIS_VHNSQ_chla_reproj.tif'

import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import geopandas as gpd
from shapely import wkt
import rioxarray as rxr

img = rasterio.open(file) 
print(img.profile)
print(img.bounds)
print(img.crs)
print(img.meta)
print(img.meta['crs'])
print(img.meta['transform'])
print('Shape:', img.shape)


rds = rxr.open_rasterio(file)
var0 = rds.name = 'chlorophyll'
img_df = rds.to_dataframe()
img_df = img_df.reset_index()
img_df = img_df.rename(columns={'x':'longitude', 'y':'latitude', 'sst':var0})
img_df = img_df.dropna()

print(img_df.head())
print(img_df.info())
#img_df.to_csv(f'{file[:-4]}.csv', index=False)


# Plot the image
#shapefile_name = 'src/data/americas_shapefile.csv'
df = pd.read_csv('src/data/trajectories.csv')

## Plot the image
plot.show(img, cmap='viridis', norm=colors.LogNorm(vmin=0.01, vmax=77), title='Chlorophyll concentration')
#
plt.colorbar(label='Chlorophyll concentration (mg/m^3)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Chlorophyll concentration (mg/m^3)')
#
## Limites
min_lat = 23
max_lat = 55
min_lon = -163
max_lon = -110

plt.xlim(min_lon, max_lon)
plt.ylim(min_lat, max_lat)

plt.savefig('src/data/2014/01/processed/2014_01_jplMURSST41_reproj.png')

from shapely import wkt
from shapely.geometry import MultiPoint
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import os

def get_years_months(file):
    df = pd.read_csv(file)
    return df[['year_month']].drop_duplicates().reset_index(drop=True)


def csv_to_geodataframe(file):
    df = pd.read_csv(file)
    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
    geo_df.crs = '+proj=longlat +datum=WGS84 +no_defs'
    return geo_df


def subset_multipoints_by_year_month(df, year, month):
    condition = (df['year'] == int(year)) & (df['month'] == int(month))
    return df['geometry'].where(condition).dropna()


def explode_multipoints(geom):
    return geom.explode(index_parts=True)


def get_coords_from_multipoints(geom):
    geom.drop_duplicates(inplace=True)
    return [(x, y) for x, y in zip(geom.x, geom.y)]


def get_rasters_list(year, month):
    raster_path = f'src/data/resampled_data/{year}/{month}'
    raster_dict = {
        'chla': 'chlor_a_resampled.tif',
        'easward_stress_bias': 'eastward_stress_bias.tif',
        'eastward_stress_sdd': 'eastward_stress_sdd.tif',
        'easward_stress': 'eastward_stress.tif',
        'easward_wind_bias': 'eastward_wind_bias.tif',
        'eastward_wind_sdd': 'eastward_wind_sdd.tif',
        'easward_wind': 'eastward_wind.tif',
        'norward_stress_bias': 'northward_stress_bias.tif',
        'northward_stress_sdd': 'northward_stress_sdd.tif',
        'norward_stress': 'northward_stress.tif',
        'norward_wind_bias': 'northward_wind_bias.tif',
        'northward_wind_sdd': 'northward_wind_sdd.tif',
        'norward_wind': 'northward_wind.tif',
        'sst': 'sst_resampled.tif'
    }
    rasters = [os.path.join(raster_path, raster) for raster in raster_dict.values()]
    return rasters

def sample_raster(coords, year, month, raster):
    # Asegurar que las muestras si correspondan a los puntos de la geometría
    values_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat'])
    values_df['year'] = [year] * len(coords)
    values_df['month'] = str(month).zfill(2)
    values_df['lon'], values_df['lat'] = zip(*coords)
    print(values_df)
    # Get value of the raster in the coordinates
    with rasterio.open(raster) as src:
        print(src.name)
        samples = list(src.sample(coords))
        # Combinar coordenadas y valores en un array de numpy
        #results = np.array([(lon, lat, val[0]) for (lat, lon), val in zip(coords, samples)])
        #print(results)
    #sst_coords = np.array(coords)
    #assert np.allclose(sst_coords, sst_samples[:, :2]), "Las coordenadas de las muestras de SST no coinciden"
    #values_df['sst'] = sst_samples[:, 2]
    #src.close()
    #return values_df

def get_sample_values(file, year, month):
    geo_df = csv_to_geodataframe(file)
    geom = subset_multipoints_by_year_month(geo_df, year, month)
    points = explode_multipoints(geom)
    coords = get_coords_from_multipoints(points)
    raster_list = get_rasters_list(year, month)
    #values_df = sample_raster(coords, sst_raster, chla_raster, ew_raster, nw_raster)
    #return values_df


yearr = 2014
monthh = 2

file = 'src/data/trajectories.csv'
dates = get_years_months(file)
geo_df = csv_to_geodataframe(file)
points = get_coords_from_multipoints(geo_df['geometry'])
raster = get_rasters_list(2014, '02')[0]
sample_raster(points, yearr, monthh, raster)
#concatenated_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst', 'chla', 'ew', 'nw'])

#for index, row in dates.iterrows():
#    year = str(row['year'])
#    month = str(row['month']).zfill(2)
#    sample_values = get_sample_values(file, year, month)
#    print('Sample values in ', year, month, ' shape: ', sample_values.shape)
#    concatenated_df = pd.concat([concatenated_df, sample_values])

#print('Concatenated shape: ', concatenated_df.shape)
#print(concatenated_df.isna().sum())
#concatenated_df.to_csv('src/data/sst_sample_values.csv', index=False)
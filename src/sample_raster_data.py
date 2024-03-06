import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import MultiPoint
import matplotlib.pyplot as plt
import rasterio

def get_years_months(file):
    df = pd.read_csv(file)
    return df[['year', 'month']]


def csv_to_geodataframe(file):
    df = pd.read_csv(file)
    geo_df = gpd.GeoDataFrame(df, geometry=df['geom'].apply(wkt.loads))
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


def sample_raster(coords, sst_raster, chla_raster, ew_raster, nw_raster):
    # Asegurar que las muestras si correspondan a los puntos de la geometría
    src = rasterio.open(sst_raster)
    values_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst', 'chla', 'ew', 'nw'])
    values_df['year'] = [year for x in coords]
    values_df['month'] = str(month)
    values_df['lon'] = [x for x, y in coords]
    values_df['lat'] = [y for x, y in coords]
    values_df['sst'] = [val[0] for val in src.sample(coords)]
    src.close()
    src = rasterio.open(chla_raster)
    values_df['chla'] = [val[0] for val in src.sample(coords)]
    src.close()
    src = rasterio.open(ew_raster)
    values_df['ew'] = [val[0] for val in src.sample(coords)]
    src.close()
    src = rasterio.open(nw_raster)
    values_df['nw'] = [val[0] for val in src.sample(coords)]
    src.close()
    return values_df


#year = '2014'
#month = '02'
#

#sst_tiff = f'src/data/{year}/{month}/processed/{year}_{month}_jplMURSST41__sst.tif'

def get_sample_values(file, year, month):
    geo_df = csv_to_geodataframe(file)
    geom = subset_multipoints_by_year_month(geo_df, year, month)
    points = explode_multipoints(geom)
    coords = get_coords_from_multipoints(points)
    sst_raster, chla_raster, ew_raster, nw_raster = select_raster_file(year, month)
    values_df = sample_raster(coords, sst_raster, chla_raster, ew_raster, nw_raster)
    return values_df


def select_raster_file(year, month):
    dir = f'src/data/{year}/{month}/processed'
    sst_raster = f'{dir}/{year}_{month}_jplMURSST41_reproj.tif'
    chla_raster = f'{dir}/{year}_{month}_NESDIS_VHNSQ_chla_reproj.tif'
    ew_raster = f'{dir}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}_clipped_eastward_wind.tif'
    nw_raster = f'{dir}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}_clipped_northward_wind.tif'
    return sst_raster, chla_raster, ew_raster, nw_raster



#sst_vals = get_sample_values(file, year, month, sst_tiff)
#raster_types = ['sst', 'chlorophyll', 'eastward_wind', 'northward_wind']

file = 'src/data/trajectories.csv'
dates = get_years_months(file)
concatenated_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst', 'chla', 'ew', 'nw'])

for index, row in dates.iterrows():
    year = str(row['year'])
    month = str(row['month']).zfill(2)
    sample_values = get_sample_values(file, year, month)
    print('Sample values in ', year, month, ' shape: ', sample_values.shape)
    concatenated_df = pd.concat([concatenated_df, sample_values])

print('Concatenated shape: ', concatenated_df.shape)
print(concatenated_df.isna().sum())
concatenated_df.to_csv('src/data/sst_sample_values.csv', index=False)
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


def sample_raster(coords, raster_file):
    src = rasterio.open(raster_file)
    values_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst'])
    values_df['year'] = [year for x in coords]
    values_df['month'] = str(month)
    values_df['lon'] = [x for x, y in coords]
    values_df['lat'] = [y for x, y in coords]
    values_df['sst'] = [val[0] for val in src.sample(coords)]
    return values_df


year = '2014'
month = '02'

file = 'src/data/trajectories.csv'
sst_tiff = f'src/data/{year}/{month}/processed/{year}_{month}_jplMURSST41__sst.tif'

def get_sample_values(file, year, month, raster_file):
    geo_df = csv_to_geodataframe(file)
    geom = subset_multipoints_by_year_month(geo_df, year, month)
    points = explode_multipoints(geom)
    coords = get_coords_from_multipoints(points)
    values_df = sample_raster(coords, raster_file)
    return values_df


def select_raster_file(type, year, month):
    dir = f'src/data/{year}/{month}/processed'
    if type == 'sst':
        raster = f'{dir}/{year}_{month}_jplMURSST41_reproj.tif'
    if type == 'chlorophyll':
        raster = f'{dir}/{year}_{month}_NESDIS_VHNSQ_chla_reproj.tif'
    if type == 'eastward_wind':
        raster = f'{dir}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}_clipped_eastward_wind.tif'
    if type == 'northward_wind':
        raster = f'{dir}/cmems_obs-wind_glo_phy_my_l4_P1M_{year}{month}_clipped_northward_wind.tif'
    return raster

#raster_types = ['sst', 'chlorophyll', 'eastward_wind', 'northward_wind']

dates = get_years_months(file)

#concatenated_df = pd.DataFrame(columns=['year', 'month', 'lon', 'lat', 'sst'])
#
#for index, row in dates.iterrows():
#    year = str(row['year'])
#    month = str(row['month']).zfill(2)
#    raster_file = select_raster_file('sst', year, month)
#    sample_values = get_sample_values(file, year, month, raster_file)
#    concatenated_df = pd.concat([concatenated_df, sample_values])


import elapid
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from elapid import MaxentModel
from sklearn import metrics
from sklearn.model_selection import train_test_split
import warnings
import rasterio
import os
from sample_raster_data import get_rasters_list

# Load the data
data = pd.read_csv('src/data/trajectories.csv')
bg_data = pd.read_csv('src/data/backgound_points.csv')

def create_annots(data, bg_data, year, month):
    # Subselect points and rasters for January 2014
    data_january = data[(data['year'] == year) & (data['month'] == month)]
    rasters, labels = get_rasters_list(year=year, month=str(month).zfill(2))
    print(labels)

    # Create GeoDataFrames
    presence =  gpd.GeoDataFrame(data_january, geometry=gpd.points_from_xy(data_january['longitude'], data_january['latitude']), crs='EPSG:4326')
    background = gpd.GeoDataFrame(bg_data, geometry=gpd.points_from_xy(bg_data['longitude'], bg_data['latitude']), crs='EPSG:4326')

    # merge datasets and read the covariates at each point location
    merged = elapid.stack_geodataframes(presence, background, add_class_label=True)

    if merged.crs is None:
        merged = merged.set_crs(epsg=4326)
        merged['geometry'] = merged['geometry'].to_crs(epsg=4326)

    annotated = elapid.annotate(merged, rasters, drop_na=True, quiet=True)
    annotated['year'] = year
    annotated['month'] = month
    # Rename the columns
    for i, label in enumerate(labels):
        annotated = annotated.rename(columns={f'b{str(i+1)}': label})
    return annotated

#years = [2014,2015,2018]
years = [2014,2015,2016,2017,2018]
month = 2

annotated_list = [create_annots(data, bg_data, year, month) for year in years]
annotated = pd.concat(annotated_list, ignore_index=True)
annotated.to_csv(f'src/data/annotated_{month}.csv', index=False)

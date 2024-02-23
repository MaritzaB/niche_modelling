#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc
import geopandas as gpd
from shapely import wkt
import seaborn as sns

def select_sst_netCDf(dir, date):
    # Cambia formato de yyyy-mm-dd a yyyymmdd
    date = date.replace('-', '')
    sst_data_ext = '090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1_clipped'
    filename = f"{dir}/{date}{sst_data_ext}.nc"
    # If filename exists the open it and get lat, lon and SST, else SST = 'NA'
    nc_file = nc.Dataset(filename)
    print(nc_file.variables.keys())
    # Get lat and lon
    lat = nc_file.variables['lat'][:]
    lon = nc_file.variables['lon'][:]
    # Get SST
    sst = nc_file.variables['analysed_sst'][0][:,:]
    sst = sst - 273.15
    # Close netCDF
    nc_file.close()
    return lon, lat, sst

def select_chlc_netCDf(dir, date):
    # Cambia formato de yyyy-mm-dd a yyyymmdd
    date = date.replace('-', '')
    chlc_data_ext = 'ESACCI-OC-L3S-CHLOR_A-MERGED-1D_DAILY_4km_GEO_PML_OCx-'
    filename = f"{dir}/noaacwNPPVIIRSSQchlaMonthly_9637_0f53_01f6_U1702510691333.nc"
    # If filename exists the open it and get lat, lon and SST, else SST = 'NA'
    nc_file = nc.Dataset(filename)
    print(nc_file.variables.keys())
    # Get lat and lon
    lat = nc_file.variables['latitude'][:]
    lon = nc_file.variables['longitude'][:]
    # Get SST
    chlor_a = nc_file.variables['chlor_a'][0][:,:]
    chlor_a = chlor_a[0,:,:]
    # Close netCDF
    nc_file.close()
    return lon, lat, chlor_a

# Plot netCDF
def plot_netCDF_sst(points_df, variable, date):
    plt.figure(figsize=(12,10))
    plt.pcolor(lon, lat, variable, cmap='jet')
    plt.colorbar()
    plt.clim(0, 30)
    sns.kdeplot(data = points_df, x = points_df['longitude'], y = points_df['latitude'], fill=True, alpha=.5)
    #plt.scatter(trayectories_df['longitude'], trayectories_df['latitude'], s=0.1, c='DarkBlue')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    title = 'Sea Surface Temperature (SST) [°C]'
    plt.title(f"{title}, {date}")
    plt.savefig(f"sst_{date}.png")
    
def plot_netCDF_chlc(points_df, variable, date):
    min_lat = 25.933687
    max_lat = 51.25798
    min_lon = -158.980523
    max_lon = -114.42687
    plt.figure(figsize=(15,10))
    plt.pcolor(lon, lat, variable, cmap='viridis')
    plt.colorbar()
    plt.clim(0, 1)
    #plt.scatter(trayectories_df['longitude'], trayectories_df['latitude'], s=0.1, c='DarkBlue')
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # Zoom in on the data
    title = 'Chlorophyll Concentration (ChlC) [mg/m3]'
    plt.title(f"{title}, {date}")
    plt.savefig(f"chlc_{date}.png")


file = 'src/data/trajectories.csv'
df = pd.read_csv(file)
trayectories_df = pd.DataFrame(df)

# Fecha del netCDF
dates = trayectories_df['date'].unique()
dates_df = pd.DataFrame(dates, columns=['date'])

fecha = dates_df['date'][0]
    
# Get lat, lon and SST
#path_sst = 'src/data/sst'

#lon, lat, sst = select_sst_netCDf(path_sst, fecha)

#plot_netCDF_sst(trayectories_df, sst, fecha)

path_chlc = 'src/data/chlc/2014/01/'
lon, lat, chlor_a = select_chlc_netCDf(path_chlc, fecha)
plot_netCDF_chlc(trayectories_df, chlor_a, fecha)

#plot_netCDF_chlc(trayectories_df, chlor_a, fecha)


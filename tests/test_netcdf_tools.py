import pandas as pd
from ..src.notebooks.netcdf_tools import get_points

trayectories_df = pd.DataFrame({'date': ['2014-01-22', '2014-01-23', '2014-01-24'],
                                'longitude': [-163, -118, -162],
                                'latitude': [23, 29, 30]})

fecha = '2014-01-22'

def test_get_points():
    print(trayectories_df)
    points = get_points(trayectories_df, fecha)
    print(points)
    assert len(points) == 1
    assert points['date'].iloc[0] == fecha
    assert points['longitude'].iloc[0] == -163
    assert points['latitude'].iloc[0] == 23

def test_get_points_wrong_date():
    points = get_points(trayectories_df, '2019-01-04')
    assert len(points) == 0


from ..src.notebooks.netcdf_tools import select_netCDf

path = 'tests/data_tests/'
end_of_filename = '090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1_clipped.nc' 
date = '2014-01-22'
var_name = 'analysed_sst'

def test_select_netCDf():
    nc_file = select_netCDf(path, end_of_filename, date)
    std_out_keys = f"dict_keys(['time', 'lat', 'lon', 'analysed_sst', 'analysis_error', 'mask', 'sea_ice_fraction', 'dt_1km_data', 'sst_anomaly'])"
    assert  str(nc_file.variables.keys()) == std_out_keys

from ..src.notebooks.netcdf_tools import extract_variables_from_netCDF
import netCDF4 as nc

nc_file =  nc.Dataset(f'{path}20140122090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1_clipped.nc')

def test_extract_variables_from_sst_netCDF():
    longitude, latitude, variable = extract_variables_from_netCDF(nc_file, 'lon', 'lat', var_name)
    assert longitude.shape == (5301,)
    assert latitude.shape == (3201,)
    assert variable.shape == (1,3201, 5301)

from ..src.notebooks.netcdf_tools import get_values

def test_get_values():
    nc_file =  nc.Dataset(f'tests/data_tests/20140122090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1_clipped.nc')
    longitude, latitude, variable = extract_variables_from_netCDF(nc_file, 'lon', 'lat', var_name)
    # Important: variable is a 3D array, but we only want the first layer
    variable = variable[0,:,:]
    points = get_points(trayectories_df, fecha)
    sst_onsite = get_values(longitude, latitude, variable, var_name, points)
    assert sst_onsite['analysed_sst'].iloc[0] == 297.89

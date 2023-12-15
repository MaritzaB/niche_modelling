def get_points(trayectories_df, date):
    points = trayectories_df[trayectories_df['date'] == date]
    return points

# Get values of variables in netCDF for each point
def get_values(longitude, latitude, variable, var_name, points):
    id = []
    var_value_points = []
    for i in range(len(points)):
        # Get coordinates of point
        lon_point = points['longitude'].iloc[i]
        lat_point = points['latitude'].iloc[i]
        # Get index of point in netCDF
        lon_index = (abs(longitude - lon_point)).argmin()
        lat_index = (abs(latitude - lat_point)).argmin()
        # Get value of variable in netCDF
        value_point = variable[lat_index,lon_index]
        var_value_points.append(value_point)
    points = points.copy()
    points.loc[:,var_name] = var_value_points
    return points

def select_netCDf(filename, date, var_name):
    # If filename exists the open it and get lat, lon and SST, else SST = 'NA'
    nc_file = nc.Dataset(filename)
    print(nc_file.variables.keys())
    # Get lat and lon
    lat = nc_file.variables['lat'][:]
    lon = nc_file.variables['lon'][:]
    # Get SST
    variable = nc_file.variables[var_name][0][:,:]
    # Close netCDF
    nc_file.close()
    return lat, lon, variable

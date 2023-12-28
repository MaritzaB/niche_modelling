import netCDF4 as nc

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

def extract_variables_from_netCDF(netCDF, x_var, y_var, var_name):
    # Get variables
    longitude = netCDF.variables[x_var][:]
    latitude = netCDF.variables[y_var][:]
    variable = netCDF.variables[var_name][:]
    netCDF.close()
    return longitude, latitude, variable

def select_netCDf(path, end_of_filename, date):
    date = date.replace('-', '')
    filename = f'{path}{date}{end_of_filename}'
    print(filename)
    nc_file =  nc.Dataset(filename)
    print(nc_file.variables.keys())
    return nc_file

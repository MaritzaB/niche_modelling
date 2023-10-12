import psycopg2, psycopg2.extras
import pandas as pd
import os

db_params = {
    "dbname": "metro_cdmx",
    "user": "admin",
    "password": "password",
    "host": "postgis",
    "port": "5432",
}
def connection(db_parameters):
    try:
        connection = psycopg2.connect(**db_parameters)
        connection.set_session(readonly=True)
        print("Connection to PostgreSQL database successful!")

    except psycopg2.Error as e:
        print("Error: Could not connect to the PostgreSQL database.")
        print(e)
    
    return connection.cursor()

cur = connection(db_params)

# Database operations
query_trayectorias = '''
    select 
        id, ST_AsText(geom) as geom, 
        ST_AsEWKT(geom) as ewkt,
        date, latitude, longitude,
        name, season,
        spheroid_dist_to_colony
    from "albatros_spheroid_distance";
'''

cur.execute(query_trayectorias)
results = cur.fetchall()
column_names = [desc[0] for desc in cur.description]

# Convert data into DataFrame
trajectories_df = pd.DataFrame(results)
trajectories_df.columns = column_names
#os.mkdir('data')

trajectories_df.to_csv('src/data/trajectories.csv', index=False)
print('Data saved in data/trajectories.csv')

query_shapefile = '''
    select id, ST_AsText(geom) as geom, ST_AsEWKT(geom) as ewkt, country
    from "americas";
'''

cur.execute(query_shapefile)
shapefile = cur.fetchall()
columns_shapefile = [desc[0] for desc in cur.description]

# Convert data into DataFrame
shapefile_df = pd.DataFrame(shapefile)
shapefile_df.columns = columns_shapefile
shapefile_df.to_csv('src/data/americas_shapefile.csv', index=False)
print('Data saved in data/americas_shapefile.csv')

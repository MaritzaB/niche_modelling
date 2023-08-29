import psycopg2, psycopg2.extras
import pandas as pd

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
query = '''select * from "gps-albatros-isla-guadalupe";'''
cur.execute(query)
results = cur.fetchall()
column_names = [desc[0] for desc in cur.description]

# Convert data into DataFrame
trajectories_df = pd.DataFrame(results)
trajectories_df.columns = column_names
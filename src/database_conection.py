import psycopg2, psycopg2.extras
import pandas as pd

db_params = {
    "dbname": "metro_cdmx",
    "user": "admin",
    "password": "password",
    "host": "postgis",
    "port": "5432",
}

try:
    connection = psycopg2.connect(**db_params)
    cur = connection.cursor()
    print("Connection to PostgreSQL database successful!")

    # Your database operations go here
    query = '''select * from "gps-albatros-isla-guadalupe" limit 10;'''
    cur.execute(query)
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]

    # Convert data into DataFrame
    df = pd.DataFrame(results)
    df.columns = column_names
    print(df)

    # Close the connection when you're done working with the database
    cur.close
    connection.close()
    print("Connection closed successfully.")
except psycopg2.Error as e:
    print("Error: Could not connect to the PostgreSQL database.")
    print(e)

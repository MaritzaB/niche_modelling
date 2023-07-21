import psycopg2, psycopg2.extras

db_params = {
    "dbname": "metro_cdmx",
    "user": "admin",
    "password": "password",
    "host": "postgis",  # Replace with your database host
    "port": "5432",       # Replace with your database port (usually 5432)
}

try:
    connection = psycopg2.connect(**db_params)
    print("Connection to PostgreSQL database successful!")

    # Your database operations go here
    cur = connection.cursor()
    datos = cur.execute("select * from profesores")
    print(datos)
    # Close the connection when you're done working with the database
    connection.close()
    print("Connection closed successfully.")
except psycopg2.Error as e:
    print("Error: Could not connect to the PostgreSQL database.")
    print(e)

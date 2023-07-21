import psycopg2
from sqlalchemy import create_engine, URL, MetaData, Table

database_url = URL.create(
    "postgresql+psycopg2",
    username="admin",
    password="password",
    host="postgis:5432",
    database="metro_cdmx",
)

engine = create_engine(database_url)

metadata = MetaData()

albatross = Table('gps-albatros-isla-guadalupe', metadata, autoload=True, autoload_with=engine, schema='public')

print(metadata.columns.keys())
print(engine.table_names())


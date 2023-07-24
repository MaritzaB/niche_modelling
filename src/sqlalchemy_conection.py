import psycopg2
from sqlalchemy import create_engine, URL, MetaData, Table, select, inspect, desc

database_url = URL.create(
    "postgresql+psycopg2",
    username="admin",
    password="password",
    host="postgis",
    port= "5432",
    database="metro_cdmx",
)
# Create engine
engine = create_engine(database_url,)
inspector = inspect(engine)
table_names = inspector.get_table_names()
print(table_names)

metadata = MetaData()

albatross = Table(
    'gps-albatros-isla-guadalupe', 
    metadata, 
    autoload_with=engine, 
    schema='public'
)

metadata.reflect(bind=engine)

# Set connection
connection = engine.connect()

query = select(*[albatross.columns.date,albatross.columns.name])
query = query.order_by(desc('date'), 'name')
print(query)
results = connection.execute(query).fetchall()

print(results[:10])

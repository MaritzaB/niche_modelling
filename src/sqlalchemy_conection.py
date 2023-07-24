import psycopg2
from sqlalchemy import create_engine, URL, MetaData, Table, select, inspect, desc, func

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

# Query para ordenar fecha en orden descendente y nombre en forma ascendente
query = select(*[albatross.columns.date,albatross.columns.name])
query = query.order_by(desc('date'), 'name')
print(query)
results = connection.execute(query).fetchall()
print(results[:10])

# Query para contar distinct names
print(f'\nQuery para contar distinct names')
query = select(*[func.count(albatross.columns.name.distinct())])
print(query)
results = connection.execute(query).scalar()
print(results)

# Query para contar total de fechas por nombre
print(f'\nQuery para contar fechas por nombre')
count_dates = func.count(albatross.columns.date.distinct().label('total_dates'))
query = select(*[albatross.columns.name , count_dates])
query = query.group_by('name')
print(query)
results = connection.execute(query).fetchall()
print(results[0:])

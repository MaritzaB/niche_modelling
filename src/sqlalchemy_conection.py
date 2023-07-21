from sqlalchemy import create_engine
## jdbc:postgresql://localhost:5432/metro_cdmx
# postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"

engine = create_engine("jdbc:postgresql://localhost:5432/metro_cdmx")

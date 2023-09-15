up:
	docker network connect qgis_devtools_postgis_net 74c7f3100f7e

connection:
	python3 src/database_conection.py

disconnection:
	python3 src/database_disconnection.py

clean:
	rm --force -R src/__pycache__/
	rm --force -R images/*
	rm --force data/
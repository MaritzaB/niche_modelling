up:
	docker network connect qgis_devtools_postgis_net e9a00037d97c

connection:
	python3 src/database_conection.py

disconnection:
	python3 src/database_disconnection.py

clean:
	rm --force -R src/__pycache__/
	rm --force -R images/*
	rm --force -R src/data/
up:
	docker network connect qgis_devtools_postgis_net 1fbf0b62a2e7

connection:
	python3 src/database_conection.py

disconnection:
	python3 src/database_disconnection.py

clean:
	rm --force -R src/__pycache__/
	rm --force -R images/*
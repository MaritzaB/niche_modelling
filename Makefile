.PHONY: tests clean
up:
	docker compose up --build --detach
	docker compose exec niche-modelling_python bash -c "cd /workdir && bash"

down: 
	docker compose down
	docker system prune --force

connection:
	python3 src/database_connection.py

disconnection:
	python3 src/database_disconnection.py

clean:
	rm --force -R src/__pycache__/
	rm --force -R images/*.png
	rm --force -R figures/*.png
	rm --force -R src/notebooks/__pycache__/
	rm --force -R tests/__pycache__
	rm --force -R __pycache__
	rm --force -R .pytest_cache
	rm --force -R src/data/*/*/processed/*.aux.xml
	clear

tests:
	pytest --verbose tests/test_sample_raster_data.py
#	pytest --verbose tests/test_netcdf_tools.py
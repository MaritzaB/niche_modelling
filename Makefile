.PHONY: tests clean
up:
	docker compose run --workdir /workdir niche-modelling bash -c "cd /workdir && bash"

connection:
	python3 src/database_connection.py

disconnection:
	python3 src/database_disconnection.py

clean:
	rm --force -R src/__pycache__/
	rm --force -R images/*.png
	rm --force -R src/notebooks/__pycache__/
	rm --force -R tests/__pycache__
	rm --force -R __pycache__
	clear

tests:
	pytest --verbose tests/test_netcdf_tools.py
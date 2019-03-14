
DB_HOST = localhost
DB_NAME = buildings-db
DB_USER = buildings-user
DB_PASS = buildings-password

.PHONY: run
run:
	gunicorn --reload --bind 0.0.0.0:8000 'src:build_app()'

.PHONY: test-lint
test-lint:
	pylint -E -d E0202 ./src

.PHONY: test-inspec
test-inspec:
	inspec exec tests/inspec.rb

.PHONY: test-nose
test-nose:
	nosetests ./tests/*.py

.PHONY: install
install:
	pip install -r requirements.txt
	pip install -e .

.PHONY: uninstall
uninstall:
	pip uninstall -y buildings_api

.PHONY: reinstall
reinstall: uninstall install

.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf dist
	rm -rf src/__pycache__
	rm -rf tests/__pycache__

# Quality of life helper for connecting to your database.
.PHONY: db-shell
db-shell:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

# Initializes the database with the schema only
.PHONY: db-init
db-init:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/schema.sql

# Intializes the database with data. Assumes the schema has already been appied
.PHONY: db-load
db-load:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/data.sql

# Drops the buildings table from the database if it exists
.PHONY: db-drop
db-drop:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f sql/revert.sql
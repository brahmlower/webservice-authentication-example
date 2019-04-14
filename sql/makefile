
# Quality of life helper for connecting to your database.
.PHONY: shell
shell:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

# Initializes the database with the schema only
.PHONY: init
init:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f ../sql/schema.sql

# Intializes the database with data. Assumes the schema has already been appied
.PHONY: load
load:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f ../sql/data.sql

# Drops the buildings table from the database if it exists
.PHONY: drop
drop:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME) -f ../sql/revert.sql

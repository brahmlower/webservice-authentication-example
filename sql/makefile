
DB_HOST = localhost
DB_NAME = buildings_db
DB_USER = admin_user
DB_PASS = admin_user_password
DB_SERVICE_USER = service_user
DB_SERVICE_PASS = service_user_password

# Quality of life helper for connecting to your database.
.PHONY: shell
shell:
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

.PHONY: shell-service
shell-service:
	PGPASSWORD=${DB_SERVICE_PASS} psql -U ${DB_SERVICE_USER} -h ${DB_HOST} -d ${DB_NAME}

# Initializes the database with the schema only
.PHONY: deploy
deploy:
	sqitch deploy pg

# Drops the buildings table from the database if it exists
.PHONY: revert
revert:
	sqitch revert pg


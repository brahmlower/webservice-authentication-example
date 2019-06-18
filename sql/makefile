
DB_HOST = localhost
DB_NAME = buildings_db
DB_USER = admin_user
DB_PASS = admin_user_password
DB_SERVICE_USER = service_user
DB_SERVICE_PASS = service_user_password

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Quality of life helper for connecting to your database.
.PHONY: shell
shell: ## Enter psql shell as the admin user
	PGPASSWORD=$(DB_PASS) psql -U $(DB_USER) -h $(DB_HOST) -d $(DB_NAME)

.PHONY: shell-service
shell-service: ## Enter psql shell as the service user (used by api service)
	PGPASSWORD=${DB_SERVICE_PASS} psql -U ${DB_SERVICE_USER} -h ${DB_HOST} -d ${DB_NAME}

# Initializes the database with the schema only
.PHONY: deploy
deploy: ## Apply the sqitch migrations
	sqitch deploy pg

# Drops the buildings table from the database if it exists
.PHONY: revert
revert: ## Revert the sqitch migrations
	sqitch revert pg

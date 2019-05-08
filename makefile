
.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Frontend ---------------------------------------------------------------------

.PHONY: frontend-build
frontend-build: ## Build the frontend resources
	cd frontend && npm run build

.PHONY: frontend-run
frontend-run: ## Run the frontend resources locally via npm serve
	cd frontend && npm run start

# Backend ----------------------------------------------------------------------

.PHONY: backend-build
backend-build: ## Build the backend
	cd backend && make build

.PHONY: backend-run
backend-run: ## Run the backend locally via gunicorn
	cd backend && make run

# DB ---------------------------------------------------------------------------

.PHONY: db-shell
db-shell: ## Enters a psql shell on docker database
	cd sql && make shell

.PHONY: db-shell-service
db-shell-service: ## Enters a psql shell on docker database as service user
	cd sql && make shell-service

.PHONY: db-deploy
db-deploy: ## Create the database schema
	cd sql && make deploy

.PHONY: db-revert
db-revert: ## Revert the database data and schema
	cd sql && make revert

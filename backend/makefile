
.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the source distribution file. Needed for 'docker build'
	python setup.py sdist

.PHONY: run
run: ## Run the project from /src. Requires virtualenv with gunicorn
	gunicorn --reload --bind 0.0.0.0:8000 'src:build_app()'

.PHONY: test-lint
test-lint: ## Error lint source. Requires virtualenv with pylint
	pylint -E -d E0202 ./src

.PHONY: test-inspec
test-inspec: ## Run api tests with inspec (eventually replacing postman/newton)
	inspec exec tests/inspec.rb

.PHONY: test-nose
test-nose: ## Run unittests. Requires virtualenv with nose
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
clean: ## Clean out misc build artifacts
	rm -rf *.egg-info
	rm -rf dist
	rm -rf src/__pycache__
	rm -rf tests/__pycache__

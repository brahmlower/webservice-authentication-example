
.PHONY: build
build:
	python setup.py sdist

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

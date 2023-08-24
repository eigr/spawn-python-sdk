# Variables
PYTHONPATH := $(shell pwd)

build:
	poetry build

install:
	poetry env use python3
	poetry lock
	poetry install

test: clean
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=unittest poetry run -vvv -m pytest

test-all:
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=local python -m pytest tests

update-poetry-and-all-dependencies:
	poetry self update
	poetry self add poetry-plugin-up
	poetry up --latest

clean:
	@find . | egrep '.pyc|.pyo|pycache' | xargs rm -rf
	@find . | egrep '.pyc|.pyo|pycache|pytest_cache' | xargs rm -rf
	@rm -rf ./htmlcov
	@rm -rf ./pycache
	@rm -rf ./pycache
	@rm -rf ./.pytest_cache
	@rm -rf ./.mypy_cache
	@find . -name 'unit_test.db' -exec rm -r -f {} +
	@find . -name '.coverage' -exec rm -r -f {} +

run:
	poetry run python3 example/spawn_example.py

run-dependencies:
	docker-compose up -d && docker-compose logs -f

stop-dependencies:
	docker-compose down

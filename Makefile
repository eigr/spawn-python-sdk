# Variables
PYTHONPATH := $(shell pwd)

linter: format
	poetry run bandit . && poetry run flake8 . && poetry run black --check .

format:
	poetry run isort . && poetry run black .

build:
	poetry build

install:
	poetry env use python3
	poetry lock
	poetry install

test: clean
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=unittest poetry run -vvv coverage run -vvv -m pytest

test-all:
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=local python -m pytest tests

update-poetry-and-all-dependencies:
	poetry self update
	poetry self add poetry-plugin-up
	poetry up --latest
	opentelemetry-bootstrap -a install

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

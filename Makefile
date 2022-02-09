.PHONY:	fmt check test clean

init:
	poetry install

fmt:
	poetry run zimports -m stock-market,tests src tests
	poetry run black src tests

check:
	poetry run flake8
	poetry export -f requirements.txt | poetry run safety check --stdin
	poetry run mypy --strict --pretty src tests

test:
	poetry run pytest

clean:
	find . -name "*pyc" -o -name "*pyo" | xargs rm
	find . -name "__pycache__" | xargs rmdir

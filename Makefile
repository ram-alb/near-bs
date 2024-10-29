install:
	poetry install

isort:
	poetry run isort near_bs

format: isort
	poetry run black near_bs

lint:
	poetry run flake8 near_bs

.PHONY: install isort format lint
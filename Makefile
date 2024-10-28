install:
	poetry install

isort:
	poetry run isort near_bs

format: isort
	poetry run black near_bs

.PHONY: install format
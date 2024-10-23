install:
	poetry install

format:
	poetry run black near_bs

.PHONY: install format
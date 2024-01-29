default: help

test: # Run tests
	poetry run python -m unittest discover app/tests

dev: # Run dev server
	poetry run uvicorn app.main:app --reload --log-level debug

prod: # Run prod server
	poetry run uvicorn app.main:app --log-level info

upgrade-deps: # Upgrade poetry dependencies
	poetry up --latest

showoutdated: # Show outdated Poetry packages
	poetry show --outdated -T

migrate: # Create migration
	poetry run alembic revision -m
	poetry run alembic upgrade head

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


.DEFAULT_GOAL := help

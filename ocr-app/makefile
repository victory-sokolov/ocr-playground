default: help

install: ## Install dependencies
	poetry install --no-root

test: # Run tests
	poetry run python -m unittest discover app/tests

dev: # Run dev server
	poetry run python main.py

prod: # Run prod server
	poetry run python main.py --log-level info

upgrade-deps: # Upgrade poetry dependencies
	poetry up --latest

showoutdated: # Show outdated Poetry packages
	poetry show --outdated -T

migrate: # Create migration
	poetry run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"
	poetry run alembic upgrade head

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


.DEFAULT_GOAL := help

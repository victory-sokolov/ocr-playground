default: help

PYTHON_VERSION_FILE := .python-version

install: # Install dependencies
	poetry env use $(shell cat $(PYTHON_VERSION_FILE))
	poetry install --no-root

test: # Run tests
	poetry run python -m unittest discover app/tests

mypy:
	poetry run mypy --config-file pyproject.toml app --cache-fine-grained

worker: # Run Celery worker
	poetry run celery -A worker.app worker --loglevel=info

worker-dev: # Run Celery worker in dev environment
	poetry run watchmedo auto-restart --directory=./ --patterns="*.py" --recursive --command='sh -c "celery -A worker.app worker --loglevel=INFO"'

flower: # Web UI for Celery (runs on port :5555)
	poetry run celery -A worker.app flower

dev: # Run dev server
	poetry run python server.py

prod: # Run prod server
	poetry run gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

upgrade-deps: # Upgrade poetry dependencies
	poetry up --latest

showoutdated: # Show outdated Poetry packages
	poetry show --outdated -T

migrate: # Create migration
	poetry run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"
	poetry run alembic upgrade head

down: # docker compose down
	docker-compose down --volumes --remove-orphans

build: # Build without cache for COPY command
	docker build --no-cache --build-arg CACHE_BUST=$(date +%s) -t ocrapp .

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.DEFAULT_GOAL := help

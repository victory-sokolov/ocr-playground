test: ## Run tests
	poetry run python -m unittest discover app/tests

dev: ## Run dev server
	poetry run uvicorn app.main:app --reload --log-level debug

upgrade-deps: ## Upgrade poetry dependencies
	poetry up --latest

showoutdated: ## Show outdated Poetry packages
	poetry show --outdated -T

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.DEFAULT_GOAL := help

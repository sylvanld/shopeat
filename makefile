SHOPEAT_AMQP_BROKER_URL	?= amqp://toto@localhost
SHOPEAT_DATABASE_URL	?= sqlite+aiosqlite:///:memory:
SHOPEAT_JWT_SECRET		?= example

export

# variables used ore modified by makefile only
VENV=.venv
PATH := $(VENV)/bin:$(PATH)

SOURCE_PATH=shopeat/
TESTS_PATH=tests/

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN { FS = ":.*?## " } /^##@/ { printf "\n%s\n", substr($$0, 5) } /^[a-zA-Z_-]+:.*?## / { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

##@ Target to work with python code locally

serve: ## Run api in debug mode with hot reload
	uvicorn shopeat.api.asgi:app --reload

format: ## Format code accorting to project conventions
	isort --profile black $(SOURCE_PATH) $(TESTS_PATH)
	black $(SOURCE_PATH) $(TESTS_PATH)

freeze: ## Show installed dependencies
	@echo "# Using pip: `which pip`"
	pip freeze

##@ Target used to test codebase quality and non-regression

test: ## Run unit tests
	 python -m pytest -v $(TESTS_PATH)

lint: ## Check for errors in code and abort if one is found
	python -m pylint $(SOURCE_PATH) || pylint-exit $?

lint-strict: ## Check for bad practices in code and abort if one is found
	isort --check --profile black $(SOURCE_PATH) $(TESTS_PATH)
	black --check $(SOURCE_PATH) $(TESTS_PATH)
	python -m pylint $(SOURCE_PATH) || pylint-exit --error-fail --warn-fail --refactor-fail $$? 

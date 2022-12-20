SHOPEAT_AMQP_BROKER_URL	?= amqp://toto@localhost
SHOPEAT_DATABASE_URL	?= sqlite+aiosqlite:///db.sqlite
SHOPEAT_JWT_SECRET		?= example

export

# variables used ore modified by makefile only
VENV=.venv
PATH := $(VENV)/bin:$(PATH)

SOURCE_PATH=shopeat/
UNIT_TESTS_PATH=tests/

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN { FS = ":.*?## " } /^##@/ { printf "\n%s\n", substr($$0, 5) } /^[a-zA-Z_0-9-]+:.*?## / { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

##@ Target to work with python code locally

serve: ## Run api in debug mode with hot reload
	uvicorn shopeat.api.asgi:app --reload

docs: ## Serve documentation with dev. server in hot relaod mode
	mkdocs serve -a 127.0.0.1:8086

format: ## Format code accorting to project conventions
	isort --profile black $(SOURCE_PATH) $(UNIT_TESTS_PATH)
	black $(SOURCE_PATH) $(UNIT_TESTS_PATH)

freeze: ## Show installed dependencies
	@echo "# Using pip: `which pip`"
	pip freeze

openapi: ## output openapi specs
	@python -m shopeat api-specs --no-info

##@ Target used to test codebase quality and non-regression

unit-tests: ## Run unit tests
	python -m pytest -v $(UNIT_TESTS_PATH)

VENOM_VAR_API_URL=http://localhost:8000

e2e-tests: ## Run end to end tests
	TEST_SETS=`find tests/e2e/*.venom.yml`		\
		&& venom run -vvv --format xml			\
			--var-from-file tests/e2e/vars.yml	\
			--output-dir tests/e2e/results		\
			$$TEST_SETS \
			

lint: ## Check for errors in code and abort if one is found
	python -m pylint $(SOURCE_PATH) || pylint-exit $$?

lint-strict: ## Check for bad practices in code and abort if one is found
	isort --check --profile black $(SOURCE_PATH) $(UNIT_TESTS_PATH)
	black --check $(SOURCE_PATH) $(UNIT_TESTS_PATH)
	python -m pylint $(SOURCE_PATH) || pylint-exit --error-fail --warn-fail --refactor-fail $$? 

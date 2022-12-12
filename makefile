SOURCE_PATH=shopeat/
TESTS_PATH=tests/

test:
	SHOPEAT_DATABASE_URL=sqlite+aiosqlite:///:memory: SHOPEAT_JWT_SECRET=example SHOPEAT_AMQP_BROKER_URL=null python -m pytest -v $(TESTS_PATH)

lint:
	python -m pylint $(SOURCE_PATH)

format:
	isort $(SOURCE_PATH) $(TESTS_PATH)
	black $(SOURCE_PATH) $(TESTS_PATH)

run:
	poetry run uvicorn backend_test.app:app --reload

fmt:
	ruff check -s --fix --exit-zero .

lint list_strict:
	mypy .
	ruff check .

lint_fix: fmt lint

migrate:
	poetry run python -m yoyo apply -vvv --batch --database "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_NAME}" ./migrations

rollback_migrations:
	poetry run python -m yoyo rollback -vvv --database "postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB_NAME}" ./migrations

test:
	pytest
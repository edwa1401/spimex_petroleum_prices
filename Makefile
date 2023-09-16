
-include .env
export

db.migrate:
		@alembic upgrade head


db.migration.create:
		@alembic revision --autogenerate -m "${name}"

style: 
	flake8 .

types:
	mypy .

tests:
	pytest --lf -vv .

check:
	make style types tests

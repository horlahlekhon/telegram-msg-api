clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	pip install pipenv
	pipenv shell --three
	pipenv install
	psql -U postgres -d telegram -f schema.sql

run:
	export QUART_APP=app:app
	quart run

all:
	install run
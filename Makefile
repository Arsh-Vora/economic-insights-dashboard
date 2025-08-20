.PHONY: build run lint clean

build:
	docker-compose build

run:
	docker-compose up

lint:
	docker-compose run --rm app ruff check .

clean:
	docker-compose down --volumes --rmi all
run:
	docker compose up

build-run:
	docker compose up -d --build

build-run-verbose:
	docker compose up --build

prod-run:
	docker compose up -d --build parser_prod admin_prod

dev-build:
	docker compose up --build parser_dev admin_dev

dev-run:
	docker compose up parser_dev admin_dev

dev-run-parser:
	docker compose up parser_dev

dev-run-admin:
	docker compose up admin_dev

down:
	docker compose down

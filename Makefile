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

raw-run:
	uv run --env-file .env python main.py & \
	uv run --env-file .env python main_admin.py & \
	wait

raw-run-parser:
	uv run --env-file .env python main.py

raw-run-admin:
	uv run --env-file .env python main_admin.py

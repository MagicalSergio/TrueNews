prod-run:
# 	docker compose up -d --build app_prod admin_prod
	docker compose up -d --build admin_prod

dev-build:
	docker compose up --build app_dev admin_dev

dev-run:
	docker compose up app_dev admin_dev

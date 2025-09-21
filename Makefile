.PHONY: db backend frontend dev stop logs test

COMPOSE = docker compose -f docker-compose.dev.yml

db:
	$(COMPOSE) down
	$(COMPOSE) build db
	$(COMPOSE) up -d db

backend:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	python app/gradio_app.py

dev:
	$(COMPOSE) up -d db
	(uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	 python app/gradio_app.py & \
	 wait)

stop:
	$(COMPOSE) down
	pkill -f "uvicorn app.main:app" || true
	pkill -f "python app/gradio_app.py" || true

logs:
	$(COMPOSE) logs -f

test:
	pytest

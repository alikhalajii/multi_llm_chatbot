.PHONY: db backend frontend dev stop logs

db:
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.dev.yml build db
	docker-compose -f docker-compose.dev.yml up -d db

backend:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	python app/gradio_app.py

dev:
	docker-compose -f docker-compose.dev.yml up -d db
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	python app/gradio_app.py

stop:
	docker-compose -f docker-compose.dev.yml down
	pkill -f "uvicorn app.main:app" || true
	pkill -f "python app/gradio_app.py" || true

logs:
	docker-compose -f docker-compose.dev.yml logs -f

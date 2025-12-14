.PHONY: help install run stop restart test db-shell db-logs db-check api-shell api-logs api-health
.DEFAULT_GOAL := help

# Use docker-compose file by default
COMPOSE=docker-compose

help:
	@echo ""
	@echo "==============================="
	@echo "   Available Make Commands"
	@echo "==============================="
	@echo ""
	@echo "==== Common Commands ===="
	@echo ""
	@echo "  make install      - Install or update Python dependencies"
	@echo "  make run          - Build and start Docker containers"
	@echo "  make stop         - Stop Docker containers"
	@echo "  make restart      - Restart all Docker containers"
	@echo "  make test         - Run tests using pytest"
	@echo ""
	@echo "==== Container Utilities ===="
	@echo ""
	@echo "  make db-shell     - Open Postgres interactive shell"
	@echo "  make db-logs      - Tail Postgres logs continuously"
	@echo "  make db-check     - Verify database connectivity from API container"
	@echo "  make api-shell    - Open shell inside API container"
	@echo "  make api-logs     - Tail API logs continuously"
	@echo "  make api-health   - Check API health endpoint (pretty JSON output)"
	@echo ""


install:
	uv sync
	uv lock

#  === DB dommands ===

db-shell: 
	@echo "Opening Postgres shell..."
	$(COMPOSE) exec db psql -U postgres

db-logs: 
	@echo "Tailing DB logs..."
	$(COMPOSE) logs -f db

db-check: 
	@echo "Checking DB connection..."
	$(COMPOSE) exec api python -c "from app.db import engine; conn=engine.connect(); print('DB connection OK'); conn.close()"


# === API commands ===
api-shell:
	@echo "Checking DB connection..."
	$(COMPOSE) exec api sh


api-logs:
	@echo "Tailing API logs..."
	$(COMPOSE) logs -f api

api-health:
	@echo "Checking API health endpoint..."
	@curl -s http://localhost:8000/health | python -m json.tool


# === Compose helpers ===
run:
	$(COMPOSE) up --build

stop:
	$(COMPOSE) down

restart: stop run


test:
	pytest tests/ --maxfail=1 --disable-warnings -q

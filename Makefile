.PHONY: build up down logs ps clean restart

# Default Docker Compose file
DC=docker-compose

# Build all services
build:
	$(DC) build

# Start with logs in terminal
up:
	$(DC) up

# Start in detached mode (background)
up-d:
	$(DC) up -d

# Build and start with logs
up-build:
	$(DC) up --build

# Build and start in detached mode
up-build-d:
	$(DC) up -d --build

# Stop all services
down:
	$(DC) down

# View logs
logs:
	$(DC) logs -f

# View specific service logs (usage: make logs-app or make logs-db)
logs-%:
	$(DC) logs -f $*

# List running containers
ps:
	$(DC) ps

# Remove all containers, volumes, and images
clean:
	$(DC) down -v --rmi all

# Restart all services
restart:
	$(DC) restart

# Restart specific service (usage: make restart-app or make restart-db)
restart-%:
	$(DC) restart $*

# Enter container shell (usage: make shell-app or make shell-db)
shell-%:
	$(DC) exec $* /bin/bash

# Show container status, CPU, memory usage
status:
	docker stats --no-stream

# Show detailed container info
info:
	docker inspect $(DC) ps -q

# Show running processes in containers
top:
	$(DC) top

# Show container health status
health:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"

alembic:
	alembic upgrade head

alembic-downgrade:
	alembic downgrade

alembic-revision:
	alembic revision --autogenerate -m "revision message"

alembic-stamp:
	alembic stamp head

alembic-history:
	alembic history

alembic-init:
	alembic init alembic

# Database migrations
migrate:
	$(DC) exec app alembic upgrade head

migrate-create:
	$(DC) exec app alembic revision --autogenerate -m "$(name)"

migrate-rollback:
	$(DC) exec app alembic downgrade -1

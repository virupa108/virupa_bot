#.PHONY tells Make that these targets are commands to run, not files to create.
# Without it, Make might think alembic is a file and skip running the command if
# a file named alembic exists.
.PHONY: build up down logs ps clean restart alembic alembic-create alembic-rollback alembic-history alembic-init alembic-stamp db-shell db-sizes db-backup db-restore db-connections db-kill-connections db-vacuum db-describe db-tables db-show db-count db-query db-custom generate-summaries

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

# Remove all containers
clean:
	$(DC) down

# Remove all containers, volumes, and images
clean_total:
	$(DC) down -v --rmi all

# Remove all unused containers, networks, images and volumes
prune:
	docker system prune -af --volumes

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

# Database migrations
# Database Migration Steps:
# 1. Create new migration:
#    - Run: make migrate-create name="description_of_changes"
#    - This generates migration script in alembic/versions/
#    - Review generated migration script before proceeding
#
# 2. Apply migration to database:
#    - Run: make alembic
#    - This upgrades database to latest migration
#    - Check logs for any errors
#
# 3. Verify changes:
#    - Run: make alembic-history
#    - Confirm migration is listed and applied
#
# 4. If problems occur:
#    - Run: make migrate-rollback
#    - This reverts the last migration
#    - Fix issues and try again
#
# 5. For fresh database:
#    - Run: make alembic-init
#    - Run: make alembic-stamp
#    - This initializes migration tracking

# Create new migration
alembic-create:
	$(DC) exec app alembic revision --autogenerate -m "$(name)"

# Apply pending migrations
alembic:
	$(DC) exec app alembic upgrade head

# Rollback one migration
alembic-rollback:
	$(DC) exec app alembic downgrade -1

# Show migration history
alembic-history:
	$(DC) exec app alembic history


alembic-init:
	$(DC) exec app alembic init alembic

# Mark current database as up to date without running migrations
alembic-stamp:
	$(DC) exec app alembic stamp head

# Database commands
# Enter database shell (psql)
# \dt - list tables
# \d tweets - describe tweets table
# SELECT * FROM tweets LIMIT 5; - query data
db-shell:
	$(DC) exec db psql -U user twitter_db

# Show table sizes and row counts
db-sizes:
	$(DC) exec db psql -U user twitter_db -c "\
		SELECT \
			relname as table, \
			pg_size_pretty(pg_total_relation_size(relid)) as total_size, \
			pg_size_pretty(pg_relation_size(relid)) as data_size, \
			pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as external_size \
		FROM pg_catalog.pg_statio_user_tables \
		ORDER BY pg_total_relation_size(relid) DESC;"

# Database describe commands
# Show table structure (usage: make db-describe name=tweets)
db-describe:
	$(DC) exec db psql -U user twitter_db -c "\d $(name)"

# Show all tables
db-tables:
	$(DC) exec db psql -U user twitter_db -c "\dt"

# Show specific table data (usage: make db-show name=tweets)
db-show:
	$(DC) exec db psql -U user twitter_db -c "SELECT * FROM $(name) LIMIT 5;"

# Count rows in table (usage: make db-count name=tweets)
db-count:
	$(DC) exec db psql -U user twitter_db -c "SELECT COUNT(*) FROM $(name);"

# Truncate specific table (usage: make db-truncate name=tweets)
db-truncate:
	$(DC) exec db psql -U user twitter_db -c "TRUNCATE TABLE $(name) CASCADE;"

# Fix permissions for all files in project directory
fix-perms:
	sudo chown -R $(USER):$(USER) .

# Backup database
db-backup:
	$(DC) exec db pg_dump -U user twitter_db > backups/twitter_db_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database (usage: make db-restore file=backups/filename.sql)
db-restore:
	cat $(file) | $(DC) exec -T db psql -U user twitter_db

# Show active connections
db-connections:
	$(DC) exec db psql -U user twitter_db -c "SELECT * FROM pg_stat_activity;"

# Kill all connections except your own
db-kill-connections:
	$(DC) exec db psql -U user twitter_db -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'twitter_db' AND pid <> pg_backend_pid();"

# Vacuum analyze (cleanup and optimize)
db-vacuum:
	$(DC) exec db psql -U user twitter_db -c "VACUUM ANALYZE;"

# Execute SQL query (usage: make db-query table=users)
db-query:
	$(DC) exec db psql -U user -d twitter_db -c "SELECT * FROM $(table);"

# Alternative with custom query (usage: make db-custom query="SELECT id,name FROM users")
db-custom:
	$(DC) exec db psql -U user -d twitter_db -c "$(query)"

# Generate missing summaries (usage: make generate-summaries [days=N])
generate-summaries:
	$(DC) exec app python -c 'from app.main import process_historical_summaries; process_historical_summaries(max_days=$(if $(days),$(days),None))'

# Fix frontend permissions
fix-permissions:
	sudo chown -R ${USER}:${USER} frontend/

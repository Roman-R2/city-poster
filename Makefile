include .env
export

# --- Common section ----------------------
rm-migrations-dirs:
	rm -rf city-poster/mainapp/migrations

clean-start-for-development:rm-migrations-dirs docker-down-remove-volumes docker-build-up \
makemigrations migrate createsuperuser
# --------------------------------------------

# --- Poetry section ----------------------
poetry-shell:
	poetry shell
# --------------------------------------------

# --- Docker section ----------------------
docker-down:
	docker-compose -f docker-compose.yml down --remove-orphans

docker-down-remove-volumes:
	docker-compose -f docker-compose.yml down -v --remove-orphans

docker-up:
	docker-compose -f docker-compose.yml up -d

docker-build-up:
	docker-compose -f docker-compose.yml up -d --build

docker-logs:
	docker-compose -f docker-compose.yml logs -f

# --------------------------------------------

# --- Django section ----------------------
migrate:
	docker-compose run --rm web-app sh -c "python manage.py migrate"

makemigrations:
	docker-compose run --rm web-app sh -c "python manage.py makemigrations"

createsuperuser:
	docker-compose run --rm web-app sh -c "python manage.py createsuperuser --no-input"
# --------------------------------------------

# --- Code section ----------------------
check-code:
	isort city-poster/app/ city-poster/mainapp/
	flake8 --extend-ignore E501,F401 city-poster/app/ city-poster/mainapp/
# --------------------------------------------
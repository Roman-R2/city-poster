include .env
export

# --- Common section ----------------------
rm-migrations-dirs:
	rm -rf city-poster/mainapp/migrations

clean-start-for-development:rm-migrations-dirs docker-down-remove-volumes docker-build-up \
makemigrations migrate createsuperuser run-starting-commands
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

parser-app-logs:
	docker-compose -f docker-compose.yml logs -f parser-app

web-app-cli:
	docker exec -ti ${PYTHON_CONTAINER_NAME} sh
# --------------------------------------------

# --- Django section ----------------------
migrate:
	docker-compose run --rm web-app sh -c "python manage.py migrate"

makemigrations:
	docker-compose run --rm web-app sh -c "python manage.py makemigrations mainapp"

createsuperuser:
	docker-compose run --rm web-app sh -c "python manage.py createsuperuser --no-input"

run-starting-commands:
	docker-compose run --rm web-app sh -c "python manage.py add-initial-event-categorys"
	docker-compose run --rm web-app sh -c "python manage.py add-initial-event-company-profile"
# --------------------------------------------

# --- Tests section ----------------------
parser-app-tests:
	docker-compose run --rm parser-app sh -c "python -m unittest discover -v -s tests -p '*_test.py'"

# --------------------------------------------

# --- Code section ----------------------
check-code:
	isort city-poster/app/ city-poster/mainapp/ event-parser/
	flake8 --extend-ignore E501,F401 city-poster/app/ city-poster/mainapp/ event-parser/
# --------------------------------------------
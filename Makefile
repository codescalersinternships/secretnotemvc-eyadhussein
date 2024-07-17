DOCKER_IMAGE_NAME = django-note-app-image
DOCKER_CONTAINER_NAME = django-note-app-container

create-virtualenv:
	python3 -m venv env

activate-virtualenv:
	source env/bin/activate

install-requirements:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

runserver:
	python manage.py runserver

test:
	python manage.py test

docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

docker-run:
	docker run -d -p 8000:8000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

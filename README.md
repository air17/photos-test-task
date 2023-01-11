
API Documentation available as a [Postman collection](Photos.postman_collection.json)

## Installation

### Run in Docker

1. Clone this repo `git clone https://github.com/air17/photos-test-task.git` and go to it's root folder.
2. Rename `.env.template` file in the root folder to `.env` and fill it in.
3. Run `docker compose up -d`
4. Optional: create admin user with a command `docker exec -it tinder python manage.py createsuperuser`

### Install for development

0. Install `python3`
1. Clone this repo `git clone https://github.com/air17/photos-test-task.git` and go to it's root directory.
2. Install dependencies: `pip install -r requirements.txt` and `pip install -r requirements-dev.txt`
3. Run `pre-commit install` and `pre-commit install --hook-type pre-push` to set up Git hooks
4. Setup PostgreSQL Database
5. Rename `.env.template` to `.env` in `photos/config` directory and fill it in.
6. Run `python manage.py makemigrations`
7. Run `python manage.py migrate`
8. Run `python manage.py runserver`

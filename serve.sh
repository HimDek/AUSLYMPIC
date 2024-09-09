#!/bin/bash

python -m venv env
source env/bin/activate

cd src

npm install
npm run scss

python manage.py makemigrations
python manage.py migrate
python manage.py dumpdata > fixtures-backup.json
python manage.py collectstatic --no-input

gunicorn --workers 3 --bind 127.0.0.1:8000 main.wsgi
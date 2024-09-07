#!/bin/bash
dotenv -e .env bash
source env/bin/activate
cd src
npm i
npm run scss
python manage.py migrate
python manage.py collectstatic
gunicorn --workers 3 --bind 127.0.0.1:8000 main.wsgi
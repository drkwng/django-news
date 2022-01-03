#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8000 --reload -w 4 super_news.wsgi

python manage.py check_permissions
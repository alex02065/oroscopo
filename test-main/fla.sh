#!/bin/bash

while !</dev/tcp/db/5432; do sleep 1; done;

python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput

echo ":not_and_bolt: Running python manage.py runserver 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000

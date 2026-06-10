#!/bin/bash

while !</dev/tcp/db/5432; do sleep 1; done;

python backend/manage.py migrate
python backend/manage.py compilemessages
python backend/manage.py collectstatic --noinput

echo ":not_and_bolt: Running python backend/manage.py runserver 0.0.0.0:8000"
python backend/manage.py runserver 0.0.0.0:8000

#!/bin/bash

# Stop execution on any error
set -o errexit

# Install required dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
    python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL" --username "$DJANGO_SUPERUSER_USERNAME" --password "$DJANGO_SUPERUSER_PASSWORD"
fi

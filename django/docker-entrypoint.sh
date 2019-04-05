#!/bin/sh

echo "Running migrations..."
# Perform database migrations
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
# Load necessary fixtures
echo "Loading Fixtures..."
python manage.py loaddata auth-group
python manage.py loaddata auth-user
python manage.py loaddata knowledgearea
python manage.py loaddata participationrole

# Start Server
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ini --py-autoreload 1

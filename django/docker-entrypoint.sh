#!/bin/sh

alias python="python3"

echo "Running migrations..."
# Perform database migrations
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
# Load necessary fixtures
echo "Loading Fixtures..."
# python manage.py loaddata auth.permission TODO: BROKEN
# python manage.py loaddata auth.group TODO: BROKEN
python manage.py loaddata backend.user
python manage.py loaddata backend.answer
python manage.py loaddata backend.knowledgearea
python manage.py loaddata backend.participationrole
python manage.py loaddata backend.projectphase
# python manage.py loaddata backend.question
# python manage.py loaddata backend.questionv2


# Start Server
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ini --py-autoreload 1

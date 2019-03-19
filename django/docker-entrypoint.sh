#!/bin/sh

echo "Running migrations..."
# Perform database migrations
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
# Load necessary fixtures
echo "Loading Fixtures..."
python loaddata auth-group
python loaddata auth-user
python loaddata knowledgearea
python loaddata participationrole
# echo "from backend.models import User; \
# User.objects.create_superuser('admin', 'admin@localhost', '123456')" \
# | python manage.py shell

# Start Server
uwsgi --ini uwsgi.ini --py-autoreload 1

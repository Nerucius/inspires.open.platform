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
# echo "from backend.models import User; \
# User.objects.create_superuser('admin', 'admin@localhost', '123456')" \
# | python manage.py shell

# Start Server
uwsgi --ini uwsgi.ini
# uwsgi --ini uwsgi.ini --py-autoreload 1

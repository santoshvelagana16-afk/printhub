#!/usr/bin/env bash
set -o errexit

echo ">>> Installing dependencies..."
pip install -r requirements.txt

echo ">>> Collecting static files..."
python manage.py collectstatic --no-input

echo ">>> Running migrations..."
python manage.py migrate --no-input

echo ">>> Loading fixture data..."
python manage.py shell -c "
from services.models import Service
if not Service.objects.exists():
    from django.core.management import call_command
    call_command('loaddata', 'services/fixtures/initial_data.json')
    print('Fixtures loaded.')
else:
    print('Data already exists, skipping fixtures.')
"

echo ">>> Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
from users.models import UserProfile
import os
u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@printhub.in')
if not User.objects.filter(username=u).exists():
    user = User.objects.create_superuser(u, e, p)
    UserProfile.objects.get_or_create(user=user)
    print(f'Superuser created: {u}')
else:
    print(f'Superuser already exists: {u}')
"

echo ">>> Build complete!"

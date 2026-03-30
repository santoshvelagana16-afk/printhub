#!/usr/bin/env python3
"""
PrintHub – Automated Setup Script
Run this once after cloning / unzipping the project.
"""
import os, sys, subprocess

def run(cmd, **kw):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, **kw)
    if result.returncode != 0:
        print(f"ERROR running: {cmd}")
        sys.exit(1)
    return result

def main():
    print("=" * 60)
    print("  PrintHub – Setup Script")
    print("=" * 60)

    # 1. Install dependencies
    print("\n[1/5] Installing Python dependencies...")
    run("pip install django pillow --break-system-packages -q || pip install django pillow -q")

    # 2. Run migrations
    print("\n[2/5] Running database migrations...")
    run("python manage.py makemigrations users services orders")
    run("python manage.py migrate")

    # 3. Load fixture data
    print("\n[3/5] Loading sample data...")
    run("python manage.py loaddata services/fixtures/initial_data.json")

    # 4. Create superuser
    print("\n[4/5] Creating admin superuser...")
    create_super = """
import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'printhub.settings'
django.setup()
from django.contrib.auth.models import User
from users.models import UserProfile
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@printhub.in', 'admin123')
    UserProfile.objects.get_or_create(user=u)
    print('  Superuser created: admin / admin123')
else:
    print('  Superuser already exists')
"""
    run(f'python -c "{create_super}"')

    # 5. Collect static
    print("\n[5/5] Collecting static files...")
    run("python manage.py collectstatic --noinput -v 0")

    print("\n" + "=" * 60)
    print("  ✅  Setup complete!")
    print("=" * 60)
    print("\n  Run the server:")
    print("    python manage.py runserver")
    print("\n  Open in browser:")
    print("    http://127.0.0.1:8000/")
    print("\n  Admin panel:")
    print("    http://127.0.0.1:8000/admin/")
    print("    Username: admin  |  Password: admin123")
    print("=" * 60)

if __name__ == "__main__":
    main()

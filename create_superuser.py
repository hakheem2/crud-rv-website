# create_superuser.py
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "franklin_used_rv.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Read superuser info from environment variables
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

# Only create if it doesn’t exist
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists or missing environment variables.")

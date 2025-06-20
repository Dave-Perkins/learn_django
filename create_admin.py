import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = "michelle"
password = "michelle"
email = "michelle@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created with password '{password}'.")
else:
    print(f"Superuser '{username}' already exists.")

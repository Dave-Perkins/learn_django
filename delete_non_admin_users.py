import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
admin_username = "michelle"

users_to_delete = User.objects.exclude(username=admin_username)
count, _ = users_to_delete.delete()
print(f"Deleted {count} user(s) (excluding '{admin_username}').")

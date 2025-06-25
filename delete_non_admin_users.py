import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from hello.models import CustomUser, SharedAccount
from django.contrib.auth import get_user_model

User = get_user_model()

# Delete all users except admin (username 'michelle' or is_superuser)
users_to_delete = User.objects.exclude(is_superuser=True).exclude(username='michelle')
user_count = users_to_delete.count()
users_to_delete.delete()

# Delete all shared accounts
shared_accounts_count = SharedAccount.objects.count()
SharedAccount.objects.all().delete()

print(f"Deleted {user_count} user(s) (excluding 'michelle' and superusers). Deleted {shared_accounts_count} shared account(s).")

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

import django
django.setup()

from hello.models import CareMessage

CareMessage.objects.filter(shared_account__isnull=True).delete()
print("All CareMessage records with null shared_account deleted.")

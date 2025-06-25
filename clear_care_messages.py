import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

import django
django.setup()

from hello.models import CareMessage

CareMessage.objects.all().delete()
print("All CareMessage records deleted.")

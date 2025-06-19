import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')

import django
django.setup()

from hello.models import LogMessage, CareMessage

LogMessage.objects.all().delete()
CareMessage.objects.all().delete()
print("All messages and comments deleted.")
from django.db import models
from django.contrib.auth.models import AbstractUser

class SharedAccount(models.Model):
    name = models.CharField(max_length=150, unique=True)
    # Optionally, add other fields for the shared account
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # Each user can belong to one shared account (change to ManyToMany if needed)
    shared_account = models.ForeignKey(SharedAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    # Add any custom fields here
    pass

# ...existing code for CareMessage, LogMessage, Comment...

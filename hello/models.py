from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class SharedAccount(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    shared_account = models.ForeignKey(SharedAccount, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='users')
    # Add any custom fields here

    pass


class CareMessage(models.Model):
    shared_account = models.OneToOneField('hello.SharedAccount', on_delete=models.CASCADE, related_name='care_message')
    message = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CareMessage for {self.shared_account.name if self.shared_account else 'Unknown'}"


class LogMessage(models.Model):
    user = models.ForeignKey('hello.CustomUser', on_delete=models.CASCADE, related_name='log_messages', null=True,
                             blank=True)
    message = models.TextField(blank=True)
    log_date = models.DateTimeField("date logged")
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)

    def __str__(self):
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y')}"

class Comment(models.Model):
    post = models.ForeignKey('LogMessage', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('hello.CustomUser', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.id} at {self.created_at.strftime('%A, %d %B, %Y')}"

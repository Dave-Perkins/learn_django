
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Add any custom fields here, for example:
    # bio = models.TextField(blank=True)
    pass
from django.utils import timezone

class LogMessage(models.Model):
    user = models.ForeignKey('hello.CustomUser', on_delete=models.CASCADE, related_name='log_messages', null=True, blank=True)
    message = models.TextField()
    log_date = models.DateTimeField("date logged")
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X') }"

class Comment(models.Model):
    post = models.ForeignKey('LogMessage', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('hello.CustomUser', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.id} at {self.created_at}"

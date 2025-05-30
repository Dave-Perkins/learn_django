from .models import Comment
from django import forms
from hello.models import LogMessage

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "image")
        labels = {
            "text": "New Comment",
        }

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message", "image")   # Add image field to the form

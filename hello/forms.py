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
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 6,
                "cols": 50,
                "class": "large-textarea",
                "style": "font-size:1.5em; font-family:inherit; line-height:1.3; padding:8px; box-sizing:border-box; border:3px solid #888; border-radius:4px;",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "log-form",  # Use the same class as the main message form
                "style": "font-size:1.33em; padding:0.51em 1.275em; border-radius:6px; height:auto; min-width:0; max-width:none;",  # Match .log-form input[type='file']
            }),
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 6,
                "cols": 50,
                "class": "large-textarea",
                "style": "font-size:1.5em; font-family:inherit; line-height:1.3; padding:8px; box-sizing:border-box; border:3px solid #888; border-radius:4px;",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "comment-form",
                "style": "font-size:1.33em; padding:0.3em;",
            }),
        }

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message", "image")   # Add image field to the form
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 8,
                "cols": 60,
                "class": "large-textarea",
                "style": "font-size:1.5em; font-family:inherit; line-height:1.3; padding:8px; box-sizing:border-box; border:3px solid #888; border-radius:4px;",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "log-form",
                "style": "font-size:1.33em; padding:0.51em 1.275em; border-radius:6px; height:auto; min-width:0; max-width:none;",
            }),
        }

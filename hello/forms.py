from django import forms
from .models import CareMessage

class CareMessageForm(forms.ModelForm):
    class Meta:
        model = CareMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 8, 'cols': 60, 'class': 'large-textarea'}),
        }

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from hello.models import SharedAccount

class CustomUserCreationForm(UserCreationForm):
    shared_account = forms.CharField(label="Shared account (horse name)", max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)
        shared_account_name = self.cleaned_data['shared_account'].strip()
        shared_account, _ = SharedAccount.objects.get_or_create(name=shared_account_name)
        user.shared_account = shared_account
        if commit:
            user.save()
        return user

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False

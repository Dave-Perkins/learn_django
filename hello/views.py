from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "hello/register.html", {"form": form})
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from hello.forms import LogMessageForm, CommentForm
from hello.models import LogMessage, Comment
from django.db import models


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage


    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return LogMessage.objects.none()
        if user.is_staff or user.is_superuser:
            return LogMessage.objects.all().order_by('-log_date')
        return LogMessage.objects.filter(user=user).order_by('-log_date')

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        user = self.request.user
        # Filter comments for each message in message_list
        filtered_comments = {}
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            # Admins see all comments
            for message in context['message_list']:
                filtered_comments[message.id] = list(message.comments.all())
        elif user.is_authenticated:
            for message in context['message_list']:
                # Only show comments left by the post owner or by admins
                filtered_comments[message.id] = list(
                    message.comments.filter(
                        models.Q(user=message.user) | models.Q(user__is_staff=True) | models.Q(user__is_superuser=True)
                    )
                )
        else:
            for message in context.get('message_list', []):
                filtered_comments[message.id] = []
        context['filtered_comments'] = filtered_comments
        return context

@require_POST
@login_required
def add_comment(request, post_id):
    post = LogMessage.objects.get(pk=post_id)
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
    return redirect('home')

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

@login_required
def log_message(request):
    form = LogMessageForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.user = request.user
            message.save()
            return redirect("home")
    return render(request, "hello/log_message.html", {"form": form})
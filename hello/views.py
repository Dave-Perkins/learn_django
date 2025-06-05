from django.contrib.auth.decorators import login_required

@login_required
def edit_message(request, message_id):
    try:
        message = LogMessage.objects.get(pk=message_id, user=request.user)
    except LogMessage.DoesNotExist:
        return redirect('home')
    if request.method == 'POST':
        form = LogMessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LogMessageForm(instance=message)
    return render(request, 'hello/edit_message.html', {'form': form, 'message': message})
from hello.forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
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



# Function-based home view to handle GET and POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages

from django.core.paginator import Paginator

from django.views.decorators.http import require_http_methods
from django.template.response import TemplateResponse

@require_http_methods(["GET", "POST"])
def home(request):
    # Handle new message POST
    if request.method == "POST" and request.user.is_authenticated:
        form = LogMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.user = request.user
            message.save()
            return redirect('home')
    else:
        form = LogMessageForm()

    # Get messages for this user (or all if admin)
    user = request.user
    if not user.is_authenticated:
        message_list = LogMessage.objects.none()
    elif user.is_staff or user.is_superuser:
        message_list = LogMessage.objects.all().order_by('-log_date')
    else:
        message_list = LogMessage.objects.filter(user=user).order_by('-log_date')

    # Filter comments for each message
    filtered_comments = {}
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        for message in message_list:
            filtered_comments[message.id] = list(message.comments.all())
    elif user.is_authenticated:
        for message in message_list:
            filtered_comments[message.id] = list(
                message.comments.filter(
                    Q(user=message.user) | Q(user__is_staff=True) | Q(user__is_superuser=True)
                )
            )
    else:
        for message in message_list:
            filtered_comments[message.id] = []

    context = {
        'message_list': message_list,
        'filtered_comments': filtered_comments,
        'comment_form': CommentForm(),
        'log_message_form': form,
        'user': user,
    }
    return TemplateResponse(request, "hello/home.html", context)

@require_POST
@login_required
def add_comment(request, post_id):
    post = LogMessage.objects.get(pk=post_id)
    # Determine which button was pressed
    submit_image = 'submit_image' in request.POST
    add_comment_btn = 'add_comment' in request.POST

    # Only include image if submit_image was pressed, otherwise clear image from FILES
    files = request.FILES if submit_image else None
    form = CommentForm(request.POST, files)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        # If only Add Comment was pressed, clear image
        if add_comment_btn:
            comment.image = None
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
from django.contrib.auth.decorators import login_required
from .models import CareMessage
from .forms import CareMessageForm




# REMOVE ALL DUPLICATE DEFINITIONS OF THE CARE VIEW


# Remove all duplicate care view definitions

@login_required
def care(request):
    user = request.user
    confirmation = False
    from django.db import IntegrityError
    try:
        care_message, _ = CareMessage.objects.get_or_create(user=user)
    except IntegrityError:
        # If there are multiple CareMessages for a user, clean up and use the first
        CareMessage.objects.filter(user=user).exclude(pk=CareMessage.objects.filter(user=user).first().pk).delete()
        care_message = CareMessage.objects.filter(user=user).first()
    if request.method == 'POST':
        new_message = request.POST.get('message', '')
        care_message.message = new_message
        care_message.save()
        confirmation = True
        # After saving, redirect to GET to avoid form resubmission and ensure the latest value is shown
        return redirect('care')
    return render(request, 'hello/care.html', {
        'message': care_message.message,
        'confirmation': confirmation
    })
from django.contrib.auth.decorators import login_required

# ... (other imports and views)



from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
            # Remove this message from alerted_messages so Ask Michelle can be used again
            alerted = request.session.get('alerted_messages', [])
            if message.id in alerted:
                alerted.remove(message.id)
                request.session['alerted_messages'] = alerted
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
    user = request.user
    User = get_user_model()
    # Admin view: show list of users
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        users = User.objects.all().order_by('username')
        return TemplateResponse(request, "hello/admin_user_list.html", {"users": users})

    # Regular user view (existing logic)
    if request.method == "POST" and user.is_authenticated:
        # If the Ask Michelle button was pressed for a previous message (not the main form)
        if 'alert_admin' in request.POST and 'message' in request.POST and not request.POST.get('id_message'):
            # Find the message object by content and user (since only the user's own messages have the button)
            message_text = request.POST.get('message', '').strip()
            image_val = request.POST.get('image', '').strip()
            # Find the most recent message with this content and user
            message_obj = LogMessage.objects.filter(user=user, message=message_text).order_by('-log_date').first()
            if message_obj:
                from django.core.mail import mail_admins
                mail_admins(
                    subject="User requested admin attention",
                    message=f"User {user.username} pressed the 'Ask Michelle' button.\nMessage content: {message_obj.message}"
                )
                # Track which message was alerted in the session
                if 'alerted_messages' not in request.session:
                    request.session['alerted_messages'] = []
                alerted = request.session['alerted_messages']
                if message_obj.id not in alerted:
                    alerted.append(message_obj.id)
                    request.session['alerted_messages'] = alerted
            return redirect('home')
        # Main form: log a new message (with or without Ask Michelle)
        form = LogMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.log_date = datetime.now()
            message_obj.user = user
            message_obj.save()
            # If the Ask Michelle button was pressed on the main form, also send an email and track
            if 'alert_admin' in request.POST:
                from django.core.mail import mail_admins
                mail_admins(
                    subject="User requested admin attention",
                    message=f"User {user.username} pressed the 'Ask Michelle' button.\nMessage content: {message_obj.message}"
                )
                if 'alerted_messages' not in request.session:
                    request.session['alerted_messages'] = []
                alerted = request.session['alerted_messages']
                if message_obj.id not in alerted:
                    alerted.append(message_obj.id)
                    request.session['alerted_messages'] = alerted
            return redirect('home')
    else:
        form = LogMessageForm()

    if not user.is_authenticated:
        message_list = LogMessage.objects.none()
    else:
        message_list = LogMessage.objects.filter(user=user).order_by('-log_date')

    filtered_comments = {}
    if user.is_authenticated:
        for message in message_list:
            filtered_comments[message.id] = list(
                message.comments.filter(
                    Q(user=message.user) | Q(user__is_staff=True) | Q(user__is_superuser=True)
                )
            )
    else:
        for message in message_list:
            filtered_comments[message.id] = []

    alerted_messages = request.session.get('alerted_messages', [])
    context = {
        'message_list': message_list,
        'filtered_comments': filtered_comments,
        'comment_form': CommentForm(),
        'log_message_form': form,
        'user': user,
        'alerted_messages': alerted_messages,
    }
    return TemplateResponse(request, "hello/home.html", context)

# Admin: view a user's posts and comments
@login_required
def admin_user_detail(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')
    User = get_user_model()
    user_obj = User.objects.get(pk=user_id)
    messages = LogMessage.objects.filter(user=user_obj).order_by('-log_date')
    # Gather comments for each message
    comments_by_message = {}
    for message in messages:
        comments_by_message[message.id] = Comment.objects.filter(post=message).order_by('-created_at')
    return TemplateResponse(request, "hello/admin_user_detail.html", {
        "viewed_user": user_obj,
        "messages": messages,
        "comments_by_message": comments_by_message,
        "comment_form": CommentForm(),
        "user": request.user,
    })


@login_required
@require_POST
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

    # Redirect logic: if admin, stay on user detail page; else, go home
    if request.user.is_staff or request.user.is_superuser:
        # Find the user whose post this is
        user_id = post.user.id
        return redirect('admin_user_detail', user_id=user_id)
    else:
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
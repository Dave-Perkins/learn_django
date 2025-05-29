import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        from .forms import CommentForm
        context['comment_form'] = CommentForm()
        return context
from .models import Comment

from .forms import CommentForm

from django.views.decorators.http import require_POST

@require_POST
def add_comment(request, post_id):
    post = LogMessage.objects.get(pk=post_id)
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
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

def log_message(request):
    form = LogMessageForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    return render(request, "hello/log_message.html", {"form": form})
# Script to delete all posts and comments from the database
from hello.models import LogMessage, Comment

# Delete all comments first (to avoid FK issues), then all posts
Comment.objects.all().delete()
LogMessage.objects.all().delete()

print("All posts and comments have been deleted.")

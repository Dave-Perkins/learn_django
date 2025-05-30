# Future Task: Admin Alert on User Log Message

**Goal:**
Alert the admin when a non-admin user logs a message.

## Approaches
1. **Send an email to admins** when a new message is logged by a non-admin user (recommended, using Django's mail system).
2. Display an alert in the Django admin interface (less common, requires custom admin code).
3. Log the event to a file or dashboard for admin review.

## Implementation Plan (for email alert)
- In the `log_message` view, after saving a new message, check if the user is not staff or superuser.
- If so, use `mail_admins()` or `send_mail()` to notify the admins.
- Configure `settings.ADMINS` and email backend in `settings.py` if not already set up.

## Example (for later):
```python
from django.core.mail import mail_admins
if not request.user.is_staff and not request.user.is_superuser:
    mail_admins(
        subject="New message logged by user",
        message=f"User {request.user.username} logged a message: {message.message}"
    )
```

---
Return to this file when ready to implement admin alerts for user log messages.

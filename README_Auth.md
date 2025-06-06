# Task: Add 'Ask Michelle' Button for User Messages

**Goal:**
Allow users to alert the admin by email with a dedicated button, without replacing the existing "Add Thoughts" button.

## Implementation Plan
1. **Add a new button** to the message form (e.g., labeled "Ask Michelle") in the template, next to "Add Thoughts".
2. **Update the view** (`home` or `log_message`) to detect when the "Ask Michelle" button is pressed (e.g., by checking the button's name in `request.POST`).
3. When the button is pressed:
    - Do not create a new message.
    - Use Django's `mail_admins()` or `send_mail()` to send an email to the admin(s) with relevant context (e.g., user info, message content if present).
4. **Configure email settings** in `settings.py` if not already set:
    - Set `ADMINS` to include the admin's email, which is ananab.tilps@gmail.com
    - Set up the email backend (e.g., SMTP or console backend for dev).
5. **Keep the existing "Add Thoughts" button** and its logic unchanged.
6. Display a success/failure message to the user after sending the alert.

## Example (for later):
```python
from django.core.mail import mail_admins
if 'alert_admin' in request.POST:
    mail_admins(
        subject="User requested admin attention",
        message=f"User {request.user.username} pressed the alert button."
    )
```

---
Return to this file when ready to implement the 'Ask Michelle' button feature.


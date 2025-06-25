from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from hello.models import SharedAccount, CustomUser

class SharedAccountBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, shared_account=None, **kwargs):
        User = get_user_model()
        if username is None or password is None:
            return None
        try:
            user = User.objects.get(username=username)
            # Allow staff/superuser login without shared_account
            if user.is_staff or user.is_superuser:
                if user.check_password(password):
                    return user
            # For regular users, require shared_account
            if shared_account:
                account = SharedAccount.objects.get(name=shared_account)
                if user.shared_account == account and user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None
        except SharedAccount.DoesNotExist:
            return None
        return None

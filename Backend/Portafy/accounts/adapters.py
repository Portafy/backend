import random
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        This method is called just after a successful social login, but before
        the login is actually processed.
        """
        # If user with this email exists, connect this social account to the user
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass  # No user with this email, will create new
            
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.phone = user.phone or str(random.randint(1000000000, 9999999999))
        user.save()
        return user

class MyAccountAdapter(DefaultAccountAdapter):
    def get_phone(self, request, user=None):
        # Return a default phone number for new social users
        return ("0XXXXXXXXXXXXX", False)  # or "" if you want it empty


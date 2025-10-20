from django.conf import settings
from rest_framework import serializers
# Registration imports
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
# Password reset imports
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.forms import  AllAuthPasswordResetForm
from allauth.account.utils import user_pk_to_url_str

class RegisterSerializer(DefaultRegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    phone = serializers.CharField(required=True, max_length=20)
    
    def validate_phone(self, phone):
        return get_adapter().clean_phone(phone)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        vd = dict(getattr(self, "validated_data", {}))
        cleaned_data["first_name"] = vd.get("first_name", "")
        cleaned_data["last_name"] = vd.get("last_name", "")
        cleaned_data["phone"] = vd.get("phone", "")
        return cleaned_data

class CustomPasswordResetSerializer(PasswordResetSerializer):
    
    def frontend_url_generator(self, request, user, token):
        uid = user_pk_to_url_str(user)
        frontend_base = settings.FRONTEND_PASSWORD_RESET_URL
        return f"{frontend_base}/{uid}/{token}"
        
    def save(self):
        request = self.context.get("request")

        # Create the Django form manually
        reset_form = AllAuthPasswordResetForm(data=self.initial_data)
        if not reset_form.is_valid():
            raise serializers.ValidationError(reset_form.errors)

        # Call its save() with your overrides
        reset_form.save(
            domain_override=settings.FRONTEND_DOMAIN,  # 👈 frontend domain
            subject_template_name="account/email/password_reset_subject.txt",
            email_template_name="account/email/password_reset_email.html",
            use_https=request.is_secure(),
            from_email=None,
            request=request,
            url_generator = self.frontend_url_generator,
        )

        return self.initial_data

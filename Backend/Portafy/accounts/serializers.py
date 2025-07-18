from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    This serializer handles user creation and validation.
    """
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "password"]
        # The password field is write-only to ensure security.
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        # This method hashes the password before saving the user instance.
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer for obtaining JWT tokens.
        This serializer uses the User model to validate user credentials.
    """
    # Email is used as the username field for authentication
    username_field = User.EMAIL_FIELD
    
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        
        self.user = authenticate(**credentials)
        
        if self.user is None:
            raise serializers.ValidationError(
                'Unable to log in with provided credentials.'
            )
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['email'] = user.email
        token["username"] = user.username
        return token
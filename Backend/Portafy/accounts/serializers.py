from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    This serializer handles user creation and validation.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
        ]
        # The password field is write-only to ensure security.
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with additional profile information.
    """

    # The website_count field returns the number of websites associated with the user.
    website_count = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["website_count"]
        # extra_kwargs = {
        #     **UserSerializer().get_extra_kwargs(),
        #     "website_count": {"read_only" : True},
        # }

    def get_website_count(self, obj):
        return obj.websites.count()


    # what other things should i return in the profile serializer
    
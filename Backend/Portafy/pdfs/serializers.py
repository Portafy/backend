from rest_framework import serializers
from .models import UploadedFile


class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ["id", "user_email", "filename", "file", "uploaded_at"]
        read_only_fields = ["id", "user_email", "filename", "uploaded_at"]

    def get_user_email(self, obj):
        return obj.user.email
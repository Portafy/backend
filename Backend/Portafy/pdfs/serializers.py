from rest_framework import serializers
from .models import UploadedFile


class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = ["id", "user_email", "filename", "file", "uploaded_at"]
        read_only_fields = ["id", "user", "filename", "uploaded_at"]

    def get_user_email(self, obj):
        return obj.user.email
    
    def save(self, **kwargs):
        request = self.context["request"]
        filename = str(request.data["file"]).rsplit(".", maxsplit=1)[0]
        kwargs.update({
            "user" : request.user,
            "filename" : filename
        })
        
        return super().save(**kwargs)
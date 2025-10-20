from rest_framework import serializers

from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    has_content = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = ["id", "user_email", "filename", "file", "uploaded_at", "has_content"]
        read_only_fields = ["id", "user", "filename", "uploaded_at"]

    def get_user_email(self, obj):
        return obj.user.email
    
    def get_has_content(self, obj):
        return bool(obj.content)
    
    def create(self, validated_data):
        # Automatically set the user to the current request user
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    
class FileExtractSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ["id", "content"]
        read_only_fields = ["id"]
        
    def get_content(self, obj):
        return obj.content
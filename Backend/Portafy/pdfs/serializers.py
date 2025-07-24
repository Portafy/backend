from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import UploadedFile
from .tasks import process_pdf

class FileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = ["id", "user_email", "filename", "file", "uploaded_at"]
        read_only_fields = ["id", "user", "filename", "uploaded_at"]

    def get_user_email(self, obj):
        return obj.user.email
    
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
        import json
        try:
            text = process_pdf(obj.file.path)
            content = json.loads(text)
            
            if content:
                return content
            raise ValidationError({"error": "No valid JSON found"})
        except Exception as e:
            return {"error": str(e)}
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ThemeConfig, Website, WebsiteContent

class WebsiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteContent
        fields = ["id", "user", "content", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
        extra_kwargs = {
            "content": {"required": True},
        }

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ThemeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeConfig
        fields = [
            "id",
            "user",
            "name",
            "theme",
            "template_type",
            "config",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"user": {"required": False}}


class SimpleWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            "id",
            "title",
            "slug",
            "user",
            "file",
            "theme",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "user", "slug", "created_at"]

    def validate_file(self, file):
        if file.user_id != self.context["request"].user.id:
            raise ValidationError("you can not use pdfs uploaded by others")
        return super().validate(file)

    def validate_content(self, content):
        if content.user_id != self.context["request"].user.id:
            raise ValidationError("you can not use contents uploaded by others")
        return super().validate(content)

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user

        return super().create(validated_data)


class FullWebsiteSerializer(SimpleWebsiteSerializer):
    content = WebsiteContentSerializer(read_only=True)
    theme = ThemeConfigSerializer(read_only=True)

    class Meta(SimpleWebsiteSerializer.Meta):
        fields = SimpleWebsiteSerializer.Meta.fields

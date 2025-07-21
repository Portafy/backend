from rest_framework import serializers
from rest_framework.request import Request
from .models import Website
from django.urls import reverse

from core.utils import get_main_path


class WebContentSerializer(serializers.Serializer):
    header = serializers.CharField()
    message = serializers.CharField()
    video = serializers.SerializerMethodField()

    def get_video(self, obj):
        video_path = obj.get("video", "")
        if video_path:
            main_path = get_main_path(self.context["request"])
            full_path = f"{main_path}/media/{video_path}"
            return full_path
        return ""


class WebsiteSerializer(serializers.ModelSerializer):
    content = WebContentSerializer()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = [
            "id",
            "title",
            "slug",
            "theme",
            "type",
            "content",
            "user",
            "file",
            "has_paid_download",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]

    def get_slug(self, obj):
        request = self.context["request"]
        view_path = get_main_path(request) + reverse("websites:websites-list")
        full_path = f"{view_path}live/{obj.slug}"
        return full_path

    def save(self, **kwargs):
        request = self.context["request"]
        user = request.user
        url = f"{request.user.username}"
        kwargs.update({"user": user, "slug": url})
        return super().save(**kwargs)

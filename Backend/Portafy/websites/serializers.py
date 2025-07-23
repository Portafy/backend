from rest_framework import serializers

from .models import Website, WebsiteContent, ThemeConfig

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
        fields = ["id", "user", "name", "theme", "template_type", "config", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "user" : {"required" : False}
        }

class SimpleWebsiteSerializer(serializers.ModelSerializer):
    # content = WebContentSerializer()
    public_url = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = [
            "id",
            "title",
            "url",
            "user",
            "file",
            "theme",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "url", "file", "created_at"]

    def get_public_url(self, obj):
        request = self.context["request"]
        if request:
            full_path = request.build_absolute_uri(obj.get_absolute_url())
            return full_path
        return obj.get_absolute_url()
    
    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)




class FullWebsiteSerializer(SimpleWebsiteSerializer):
    theme_config = ThemeConfigSerializer(required=False)
    content = WebsiteContentSerializer(required=True)

    class Meta(SimpleWebsiteSerializer.Meta):
        fields = SimpleWebsiteSerializer.Meta.fields + ["content", "theme_config"]


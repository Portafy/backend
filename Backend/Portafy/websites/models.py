import uuid
from accounts.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from pdfs.models import UploadedFile


class WebsiteContent(models.Model):
    class Meta:
        verbose_name = "Website Content"
        verbose_name_plural = "Website Contents"
        ordering = ["-created_at"]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="website_contents"
    )
    content = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Content: by {self.user_id} at {self.created_at}"


class ThemeConfig(models.Model):
    class Meta:
        verbose_name = "Theme Configuration"
        verbose_name_plural = "Theme Configurations"
        ordering = ["-created_at"]

    class THEMES_CHOICES(models.TextChoices):
        DARK = "dark", "Dark"
        LIGHT = "light", "Light"

    class TEMPLATE_TYPES_CHOICES(models.TextChoices):
        MINIMAL = "minimal", "Minimal"
        CREATIVE = "creative", "Creative"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_themes",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=20, unique=True, db_index=True, default="Custom Theme"
    )
    theme = models.CharField(
        max_length=20, choices=THEMES_CHOICES.choices, default=THEMES_CHOICES.DARK
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES_CHOICES.choices,
        default=TEMPLATE_TYPES_CHOICES.MINIMAL,
    )
    config = models.JSONField(default=dict)  # Store theme-specific configurations
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Theme Config: {self.theme} - {self.template_type}"

    def delete(self, *args, **kwargs):
        if self.websites.exists():
            raise ValidationError(
                "Cannot delete ThemeConfig while it is assigned to a Website."
            )
        super().delete(*args, **kwargs)


class WebsiteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user", "file")


class Website(models.Model):
    class Meta:
        verbose_name = "Website"
        verbose_name_plural = "Websites"
        ordering = ["-created_at"]

    objects = WebsiteManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    file = models.OneToOneField(
        UploadedFile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="website",
    )
    theme = models.ForeignKey(
        ThemeConfig,
        on_delete=models.SET_NULL,
        related_name="websites",
        null=True,
        blank=True,
    )
    content = models.OneToOneField(
        WebsiteContent,
        on_delete=models.CASCADE,
        related_name="websites",
        null=True,
        blank=True,
    )

    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    slug = models.SlugField(unique=True, db_index=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def get_absolute_url(self):
        return reverse("websites:live_site", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (
                f"{self.user.username}-{slugify(self.title)}-{str(self.unique_id)[:8]}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Website: {self.title} by {self.user_id}"

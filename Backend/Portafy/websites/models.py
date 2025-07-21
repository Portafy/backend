from django.db import models
from accounts.models import User
from pdfs.models import UploadedFile
from rest_framework.exceptions import ValidationError

class Website(models.Model):
    class THEMES_CHOICES(models.TextChoices):
        DARK = "dark", "Dark"
        LIGHT = "light", "Light"

    class TYPES_CHOICES(models.TextChoices):
        MINIMAL = "minimal", "Minimal"
        CREATIVE = "creative", "Creative"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    theme = models.CharField(
        max_length=50, choices=THEMES_CHOICES.choices, default=THEMES_CHOICES.DARK
    )
    type = models.CharField(
        max_length=50, choices=TYPES_CHOICES.choices, default=TYPES_CHOICES.CREATIVE
    )
    content = models.JSONField()  # Parsed resume or manual info
    has_paid_download = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    # to ensure that the user associated with the uploaded file is the same as the user of the website
    def clean(self):
        if self.file.user != self.user:
            raise ValidationError("User mismatch: UploadedFile.user must match Website.user")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Website: {self.title} by {self.user.email}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Websites"


class Video(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="videos"
    )
    url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video: {self.title} on {self.website.title}"

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name_plural = "Videos"

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from accounts.models import User
from .validators import validate_file_size


class UploadedFile(models.Model):
    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name_plural = "Uploaded Files"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(
        upload_to="uploaded_files/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            validate_file_size,
        ],
    )
    content = models.JSONField(null=True, blank=True)
    filename = models.CharField(max_length=250)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = slugify(str(self.file).rsplit(".", maxsplit=1)[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"File: {self.filename} -- by -- user-{self.user_id}"

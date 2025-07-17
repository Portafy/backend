from django.core.exceptions import ValidationError
from django.db import models
from websites.models import Website
from accounts.models import User

# Create your models here.
class UploadedFile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # to ensure that the user associated with the uploaded file is the same as the user of the website

    def clean(self):
        if self.website.user != self.user:
            raise ValidationError("User mismatch: UploadedFile.user must match Website.user")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Uploaded File for {self.website.title}"
    

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Uploaded Files'
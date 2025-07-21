from django.db import models
from accounts.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='uploaded_files/')
    filename = models.CharField(max_length=250)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Uploaded File by {self.user.email}"

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Uploaded Files'
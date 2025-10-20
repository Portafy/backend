from django.db import models
from accounts.models import User
from websites.models import Website

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_successful = models.BooleanField(default=False)
    payment_gateway = models.CharField(max_length=20)
    reference_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.website.title} by {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Payments'
        unique_together = ('user', 'website', 'reference_id')
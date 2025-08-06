from django.db import models
from django.contrib.auth.models import AbstractUser  # pyright: ignore[reportMissingModuleSource]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    def __str__(self):
        return self.username


class Customer(models.Model):
    class SUBSCRIPTION_CHOICES(models.TextChoices):
        FREE = "F", "Free"
        BASIC = "B", "Basic"
        PRO = "P", "Pro"
        PREMIUM = "PR", "Premium"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    subscription = models.CharField(
        max_length=3,
        choices=SUBSCRIPTION_CHOICES.choices,
        default=SUBSCRIPTION_CHOICES.FREE,
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username}"

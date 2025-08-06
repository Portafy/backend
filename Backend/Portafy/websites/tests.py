from pytest import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Website, User

# Create your tests here.
class WebsiteTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_website(self):
        response = self.client.post(reverse("websites:websites-list"), data={
            "title": "Test Website",
            "theme" : 1,
            "content" : 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_website(self):
        website = Website.objects.create(
            title="Test Website",
            slug="test-website",
            user=self.user
        )
        response = self.client.get(reverse("websites:websites-detail", args=[website.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], website.title)

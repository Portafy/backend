from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User

# Create your tests here.
class AuthViewsTestCase(APITestCase):
    def setUp(self):
        self.token_refresh_url = reverse("accounts:token_refresh")
        self.register_url = reverse("accounts:register")  # Match your URL name
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")

        self.user_data = {
            "first_name": "Bella",
            "last_name": "Mekonnen",
            "username" : "bella_moka",
            "email": "bella@example.com",
            "password": "securepass123",
            "phone": "0912345678"
        }
        
        response = self.client.post(self.register_url, self.user_data, format = "json")
        self.refresh_token = response.data["refresh"]
        self.access_token = response.data["access"]
        
    def test_register_user(self):
        # already registered in setup, just verify
        user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(user.first_name, "Bella")
        self.assertTrue(user.check_password(self.user_data["password"]))
        
        
    def test_login_user(self):
        credentials = {
            "email" : self.user_data["email"],
            "password" : self.user_data["password"]
        }
        
        response = self.client.post(self.login_url, credentials, format = "json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data['user']["email"], self.user_data["email"])
        

    def test_token_refresh(self):
        response = self.client.post(self.token_refresh_url, {
            "refresh" : self.refresh_token
        }, format = "json")
        
        self.assertNotIn("refresh", response.data)
        self.assertIn("access", response.data)
        
        
    def test_logout_user(self):
        response = self.client.post(self.logout_url, {
            "refresh" : self.refresh_token
        }, format = "json")
        
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["message"], "Successfully logged out.")
        
        
    def test_logout_invalid_token(self):
        response = self.client.post(self.logout_url, {
            "refresh" : "invalidtoken"
        }, format = "json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)


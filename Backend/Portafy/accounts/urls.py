from django.urls import path
from .views import auth_views

app_name = "accounts"
urlpatterns = [
    path("google/", auth_views.GoogleLogin.as_view(), name="google_login"),
    path("github/", auth_views.GitHubLogin.as_view(), name="github_login"),
]

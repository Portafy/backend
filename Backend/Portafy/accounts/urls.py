from django.urls import path
from .views import auth_views, user_views

app_name = "accounts"
urlpatterns = [
    # authentication and registration URLs
    path("token/refresh/", auth_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/", auth_views.LoginView.as_view(), name="login"),
    path("auth/register/", auth_views.RegisterView.as_view(), name="register"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("user/password/change/", auth_views.ChangePasswordView.as_view(), name="change_password"),
    # user URLs
    path("user/profile/", user_views.UserProfileView.as_view(), name="user_profile"),
]

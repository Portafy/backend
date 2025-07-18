from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..models import User
from ..serializers import UserSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT tokens.
    This view uses the UserSerializer to validate user credentials.
    """

    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    """
    View to handle user registration.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    
class LogoutView(TokenRefreshView):
    """
    View to handle user logout.
    This view invalidates the user's refresh token.
    """

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..models import User
from ..serializers import UserSerializer


class LoginView(TokenObtainPairView):
    """
    View to handle user registration.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user_instace = User.objects.get(email = request.data.get("email"))
            user_data = UserSerializer(user_instace, context = {"request" : request}).data
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        except User.DoesNotExist as e:
            return Response({
                "message" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data
        return Response({
            "user" : user_data,
            **token    
        }, status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    """
    View to handle user registration.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        user = serializer.instance
        
        refresh = RefreshToken.for_user(user)
        token = {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }

        return Response({
            "user" : serializer.data,
            **token
        }, status=status.HTTP_201_CREATED)

class LogoutView(TokenRefreshView):
    """
    View to handle user logout.
    This view invalidates the user's refresh token.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("Token blacklisted successfully.")
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
            
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

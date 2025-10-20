from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..models import User
from ..serializers import UserSerializer

import logging

logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    """
    Handles user login and returns JWT tokens along with user data.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=request.data.get("email"))
            user_data = UserSerializer(user, context={"request": request}).data
            token = serializer.validated_data
            return Response({"user": user_data, **token}, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.error(f"Token error during login: {e}")
            raise InvalidToken(e.args[0])
        except User.DoesNotExist as e:
            logger.warning(f"User not found during login: {e}")
            return Response(
                {"message": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegisterView(CreateAPIView):
    """
    Handles user registration and returns JWT tokens along with user data.
    """

    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        token = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(
            {"user": serializer.data, **token}, status=status.HTTP_201_CREATED
        )


class LogoutView(TokenRefreshView):
    """
    Handles user logout by blacklisting the refresh token.
    """

    permission_classes = [AllowAny]
    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs) -> Response:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            logger.warning("No refresh token provided for logout.")
            return Response(
                {"message": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return Response(
                {"message": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

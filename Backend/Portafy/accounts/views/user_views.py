from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import UserProfileSerializer
from ..models import User

class UserProfileView(RetrieveUpdateAPIView):
    """
    View to retrieve and update user profile information.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']
    
    def get_object(self):
        # Return the current authenticated user
        return self.request.user
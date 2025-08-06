from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwnerOrAdminOrReadOnly

from .models import Website
from .serializers import SimpleWebsiteSerializer, FullWebsiteSerializer


class WebsiteViewSet(ModelViewSet):
    """
    ViewSet for managing Website instances.
    Provides list, create, retrieve, update, and delete actions.
    Uses different serializers for read and write operations.
    Permissions: Only owners or admins can modify, others have read-only access.
    """

    queryset = Website.objects.select_related("theme", "content").all()
    serializer_class = SimpleWebsiteSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]


class LiveSiteView(RetrieveAPIView):
    queryset = Website.objects.all()
    serializer_class = FullWebsiteSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"

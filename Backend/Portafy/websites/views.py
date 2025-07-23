from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwnerOrAdminOrReadOnly
from .models import Website
from .serializers import SimpleWebsiteSerializer, FullWebsiteSerializer


class WebsiteViewSet(ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = SimpleWebsiteSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return FullWebsiteSerializer
        return self.serializer_class


class LiveSiteView(RetrieveAPIView):
    queryset = Website.objects.all()
    serializer_class = FullWebsiteSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "url"
    lookup_field = "url"
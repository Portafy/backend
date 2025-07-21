from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Website
from .serializers import WebsiteSerializer


class WebsiteViewSet(ModelViewSet):
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Website.objects.all().select_related("user", "file")


class LiveSiteView(RetrieveAPIView):
    serializer_class = WebsiteSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(Website, slug=self.kwargs["url"])

    def retrieve(self, request, *args, **kwargs):
        website = self.get_serializer(self.get_object()).data

        context = {
            "content": {**website.get("content")},
            "theme": website.get("theme"),
            "webs_type": website.get("type"),
        }

        print()

        return render(request, "index.html", context)

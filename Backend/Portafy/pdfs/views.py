from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import UploadedFile
from .serializers import FileSerializer

from core.permissions import IsOwner


class FileViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer
    permission_classes = [IsOwner]
    queryset = UploadedFile.objects.all().select_related("user")

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics  import RetrieveAPIView

from core.permissions import IsOwner

from .models import UploadedFile
from .serializers import FileSerializer, FileExtractSerializer


class FileViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer
    permission_classes = [IsOwner]
    queryset = UploadedFile.objects.all().select_related("user")


class FileExtractView(RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = FileExtractSerializer
    permission_classes = [IsOwner]
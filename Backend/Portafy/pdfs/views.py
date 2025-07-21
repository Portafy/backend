from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from .models import UploadedFile
from .serializers import FileSerializer


class FileUploadView(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        context = self.get_serializer_context()
        filename = str(context["request"].data["file"])
        print("filename: ", filename)
        filename = filename.rsplit(".", maxsplit=1)[0]
        return serializer.save(user=context["request"].user, filename = filename)


class FileDetailView(RetrieveUpdateAPIView):
    queryset = UploadedFile.objects.all().select_related("user")
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer


class FileListView(ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = UploadedFile.objects.filter(user_id=self.request.user.id)
        return queryset

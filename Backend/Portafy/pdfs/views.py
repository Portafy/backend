import os
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status

from core.permissions import IsOwner

from .models import UploadedFile
from .serializers import FileSerializer, FileExtractSerializer
from .tasks import process_pdf


class FileViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer
    permission_classes = [IsOwner]
    queryset = UploadedFile.objects.all().select_related("user")

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return self.request.user.files.all()


class FileExtractView(RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = FileExtractSerializer
    permission_classes = [IsOwner]
    
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if not obj.content:
            try:
                import json
                text = process_pdf.delay(obj.file.path)
                content = json.loads(text)
                
                if content:
                    obj.content = content
                    obj.save()
                    
                else:
                    raise ValidationError({"error": "No valid JSON found"})
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        if os.path.exists(obj.file.path):
            os.remove(obj.file.path)
            
        
        print("file path deleted: ", obj.file)
        return super().retrieve(request, *args, **kwargs)
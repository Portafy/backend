from django.urls import path

from . import views

urlpatterns = [
    path("", views.FileListView.as_view(), name="pdfs"),
    path("upload-pdf/", views.FileUploadView.as_view(), name="upload-pdf"),
    path("<int:pk>/", views.FileDetailView.as_view(), name="pdf-detail"),
]
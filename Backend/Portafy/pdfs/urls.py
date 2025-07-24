from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.FileViewSet, basename="files")

urlpatterns = [
    path("", include(router.urls)),
    path("extract/<int:pk>/", views.FileExtractView.as_view(), name="file-extract"),
]

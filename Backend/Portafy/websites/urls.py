from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.WebsiteViewSet, basename="websites")

app_name = "websites"
urlpatterns = [
        path("",include(router.urls)),
        path("live/<slug:slug>/", views.LiveSiteView.as_view(), name = "live_site"),
]

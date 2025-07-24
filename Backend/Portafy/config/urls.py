"""
URL configuration for Portafy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from pprint import pprint

import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings

pprint(debug_toolbar.urls)

app_name = "config"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls"), name = "accounts"),  # Include URLs from the accounts app
    path("pdfs/", include("pdfs.urls"), name = "pdfs"),  # Include URLs from the PDFs app
    path("websites/", include("websites.urls"), name = "websites"),  # Include URLs from the websites app
    path("payments/", include("payments.urls"), name = "payments"),  # Include URLs from the payments app
    path("__debug__/", include(debug_toolbar.urls)),
]

# for serving the uploaded files in the media folder
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

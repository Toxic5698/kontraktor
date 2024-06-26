"""kontraktor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from operators.views import WelcomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("attachments/", include("attachments.urls"), name="attachments"),
    path("authentication/", include("authentication.urls"), name="authentication"),
    path("clients/", include("clients.urls"), name="clients"),
    path("contracts/", include("contracts.urls"), name="contracts"),
    path("emailing/", include("emailing.urls"), name="emailing"),
    path("proposals/", include("proposals.urls"), name="proposals"),
    path("documents/", include("documents.urls"), name="documents"),
    path("reports/", include("reports.urls"), name="reports"),
    path("", WelcomePageView.as_view(), name="welcome-page"),
]

admin.site.site_header = "Kontraktor admin"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

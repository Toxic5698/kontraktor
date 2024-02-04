from django.urls import path
from documents.views import *

urlpatterns = [
    path("print/<str:sign_code>/<str:type>/<int:pk>", PrintView.as_view(), name="print-document"),
    path("download/<str:sign_code>/<str:type>/<int:pk>", DownloadView.as_view(), name="download"),

]

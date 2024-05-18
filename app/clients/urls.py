from django.urls import path
from clients.views import *

urlpatterns = [
    path("", ClientsTableView.as_view(), name="clients"),
    path("edit/<str:pk>/", ClientEditView.as_view(), name="edit-client"),
    path("create/", ClientCreateView.as_view(), name="create-client"),
    path("delete/<str:pk>/", ClientDeleteView.as_view(), name="delete-client"),
    path("signing/<str:sign_code>/<str:pk>/<str:type>", SigningDocument.as_view(), name="signing-document"),
    path("create-demo", CreateDemoClient.as_view(), name="create-demo-client"),
    path("<str:sign_code>", DocumentsToSignView.as_view(), name="document-to-sign"),
]

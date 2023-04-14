from django.urls import path
from clients.views import *

urlpatterns = [
    path("", ClientsTableView.as_view(), name="clients"),
    path("edit/<int:pk>/", ClientEditView.as_view(), name="edit-client"),
    path("create/", ClientCreateView.as_view(), name="create-client"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete-client"),
    path("signing/<str:sign_code>/<int:pk>/<str:type>", SigningDocument.as_view(), name="signing-document"),
    path("<str:sign_code>", DocumentsToSignView.as_view(), name="document-to-sign"),
    path("<str:sign_code>/<str:type>/<int:pk>", DocumentView.as_view(), name="print-document")

]

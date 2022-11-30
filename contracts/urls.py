from django.urls import path
from .views import *

urlpatterns = [
    path("", ContractsTableView.as_view(), name='contracts'),
    path("create", ContractCreateView.as_view(), name="create-contract"),
    path("edit/<int:pk>", ContractUpdateView.as_view(), name="edit-contract"),
    path("delete_contract/<int:pk>", ContractDeleteView.as_view(), name="delete-contract"),
    path("delete_attachment/<int:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("<int:pk>", ContractParseView.as_view(), name="parse-contract"),
    path("edit-cores/<int:pk>", ContractCoresEditView.as_view(), name="edit-cores"),
    path("manage_attachments/<int:pk>", AttachmentUploadView.as_view(), name="manage-attachments")
]

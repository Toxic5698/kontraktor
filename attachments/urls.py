from django.urls import path
from attachments.views import *

urlpatterns = [
    path("delete_attachment/<int:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("manage_attachments/<int:pk>", AttachmentManageView.as_view(), name="manage-attachments")
]

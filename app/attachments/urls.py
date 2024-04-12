from django.urls import path
from attachments.views import *

urlpatterns = [
    path("delete/<int:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("manage/<int:pk>", AttachmentManageView.as_view(), name="manage-attachments"),
    path("add-attachment-attribute/<int:pk>", UploadedAttachmentView.as_view(), name="add-attachment-attribute"),
    path("get-uploaded/<int:pk>", UploadedAttachmentView.as_view(), name="get-uploaded"),
    path("get-default/<int:pk>", DefaultAttachmentView.as_view(), name="get-default"),
]

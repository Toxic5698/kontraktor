from django.urls import path
from attachments.views import *

urlpatterns = [
    path("delete/<str:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("manage/<str:pk>", AttachmentManageView.as_view(), name="manage-attachments"),
    path("add-attachment-attribute/<str:pk>", UploadedAttachmentView.as_view(), name="add-attachment-attribute"),
    path("get-uploaded/<str:pk>", UploadedAttachmentView.as_view(), name="get-uploaded"),
    path("get-default/<str:pk>", DefaultAttachmentView.as_view(), name="get-default"),
    path("remove-default-attachment/<str:pk>/<str:client>", DefaultAttachmentView.as_view(), name="remove-default-attachment"),
]

from django.urls import path
from attachments.views import *

urlpatterns = [
    path("delete/<int:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("manage/<int:pk>", AttachmentManageView.as_view(), name="manage-attachments"),
    path("change-purpose/<int:pk>", AttachmentManageView.as_view(), name="change-purpose")
]

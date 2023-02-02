from django.urls import path
from app.attachments.views import *

urlpatterns = [
    path("delete/<int:pk>", AttachmentDeleteView.as_view(), name="delete-attachment"),
    path("manage/<int:pk>", AttachmentManageView.as_view(), name="manage-attachments")
]

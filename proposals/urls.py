from django.urls import path

from proposals.views import *

urlpatterns = [
    path("", ProposalsTableView.as_view(), name="proposals"),
    path("upload", ProposalUploadView.as_view(), name="upload-proposal"),
    path("edit/<int:pk>", ProposalEditView.as_view(), name="edit-proposal"),
    path("delete/<int:pk>", ProposalDeleteView.as_view(), name="delete-proposal"),
    path("create", ProposalCreateView.as_view(), name="create-proposal"),

]

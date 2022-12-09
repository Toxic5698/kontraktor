from django.urls import path

from proposals.views import *

urlpatterns = [
    path("", ProposalsListView.as_view(), name="proposals"),
    path("upload", ProposalUploadView.as_view(), name="upload-proposal"),
    path("edit/<int:pk>", ProposalEditView.as_view(), name="edit-proposal"),

]

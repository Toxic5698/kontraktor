from django.urls import path

from proposals.views import *

urlpatterns = [
    path("", ProposalsTableView.as_view(), name="proposals"),
    path("create", ProposalEditView.as_view(), name="create-proposal"),
    path("create/<str:client_id>", ProposalEditView.as_view(), name="create-proposal"),
    path("edit/<str:pk>", ProposalEditView.as_view(), name="edit-proposal"),
    path("edit/payments/<str:proposal_id>", PaymentsEditView.as_view(), name="edit-payments"),
    path("delete/<str:pk>", ProposalDeleteView.as_view(), name="delete-proposal"),
    path("items/<str:pk>", ProposalItemsView.as_view(), name="edit-items"),
]

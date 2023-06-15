from django.urls import path

from proposals.views import *

urlpatterns = [
    path("", ProposalsTableView.as_view(), name="proposals"),
    path("create", ProposalEditView.as_view(), name="create-proposal"),
    path("create/<int:client_id>", ProposalEditView.as_view(), name="create-proposal"),
    path("edit/<int:pk>", ProposalEditView.as_view(), name="edit-proposal"),
    path("edit/payments/<int:proposal_id>", PaymentsEditView.as_view(), name="edit-payments"),
    path("delete/<int:pk>", ProposalDeleteView.as_view(), name="delete-proposal"),
    path("items/<int:pk>", ProposalItemsView.as_view(), name="edit-items"),
    path("send/<int:pk>", ProposalSendView.as_view(), name="send-proposal"),
    path("get-items/", ItemsList.as_view(), name="get-items"),
]

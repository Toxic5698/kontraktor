from django.urls import path
from contracts.views import *

urlpatterns = [
    path("", ContractsTableView.as_view(), name="contracts"),
    path("create/<str:proposal_id>", ContractCreateView.as_view(), name="create-contract"),
    path("edit/<str:pk>", ContractUpdateView.as_view(), name="edit-contract"),
    path("delete_contract/<str:pk>", ContractDeleteView.as_view(), name="delete-contract"),
    path("create-protocol/<str:pk>", ProtocolCreateView.as_view(), name="create-protocol"),
    path("edit-protocol/<str:pk>", ProtocolEditView.as_view(), name="edit-protocol"),
    path("get-items/", ProtocolItemListView.as_view(), name="get-items"),
    path("delete_protocol/<str:pk>", ProtocolDeleteView.as_view(), name="delete-protocol"),
]

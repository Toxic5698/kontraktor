from django.urls import path
from contracts.views import *

urlpatterns = [
    path("", ContractsTableView.as_view(), name='contracts'),
    path("create/<int:proposal_id>", ContractCreateView.as_view(), name="create-contract"),
    path("edit/<int:pk>", ContractUpdateView.as_view(), name="edit-contract"),
    path("delete_contract/<int:pk>", ContractDeleteView.as_view(), name="delete-contract"),
    path("edit-cores/<int:pk>", ContractCoresEditView.as_view(), name="edit-cores"),
    path("send/<int:pk>", ContractSendView.as_view(), name="send-contract"),

]

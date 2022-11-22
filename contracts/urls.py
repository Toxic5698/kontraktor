from django.urls import path
from .views import *

urlpatterns = [
    path("", ContractsTableView.as_view(), name='contracts'),
    path("create", ContractCreateView.as_view(), name="create-contract"),
    path("edit/<int:pk>", ContractUpdateView.as_view(), name="edit-contract"),
    path("delete/<int:pk>", ContractDeleteView.as_view(), name="delete-contract"),
    path("<int:pk>", ContractParseView.as_view(), name="parse-contract"),
]

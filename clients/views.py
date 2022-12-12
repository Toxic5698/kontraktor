from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from clients.models import Client
from clients.tables import ClientTable
from clients.filters import ClientFilter
from clients.forms import ClientForm


class ClientsTableView(SingleTableMixin, FilterView):
    table_class = ClientTable
    model = Client
    template_name = "clients/clients_list.html"
    filterset_class = ClientFilter


class ClientCreateView(CreateView):
    form_class = ClientForm
    template_name = "clients/edit_client.html"
    # TODO: only refresh form
    success_url = reverse_lazy("clients")
    model = Client


class ClientEditView(UpdateView):
    model = Client
    template_name = "clients/edit_client.html"
    form_class = ClientForm
    # TODO: only refresh form
    success_url = reverse_lazy("clients")


class ClientDeleteView(DeleteView):
    success_url = reverse_lazy("clients")
    model = Client
    template_name = "clients/confirm_delete_client.html"

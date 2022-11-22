from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .forms import ContractForm
from .models import Contract
from .tables import ContractTable
from .filters import ContractFilter


class ContractCreateView(CreateView):
    form_class = ContractForm
    template_name = "contracts/create_contract.html"
    success_url = reverse_lazy("contracts")
    model = Contract


class ContractUpdateView(UpdateView):
    form_class = ContractForm
    template_name = "contracts/create_contract.html"
    success_url = reverse_lazy("contracts")
    model = Contract


class ContractDeleteView(DeleteView):
    success_url = reverse_lazy("contracts")
    model = Contract
    template_name = "contracts/confirm_delete_contract.html"


class ContractParseView(View):

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        template = "contracts/kupni_smlouva.html" if contract.type == "KOUPE" else "contracts/smlouva_o_dilo.html"
        context = {
            "contract": contract
        }
        return TemplateResponse(request, template, context)


class ContractsTableView(SingleTableMixin, FilterView):
    table_class = ContractTable
    model = Contract
    template_name = "contracts/dashboard.html"
    filterset_class = ContractFilter

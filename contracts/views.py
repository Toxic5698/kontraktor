from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .forms import ContractForm
from .models import Contract, ContractCore
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edited_cores'] = ContractCore.objects.filter(default=False, contract=self.object)
        return context


class ContractDeleteView(DeleteView):
    success_url = reverse_lazy("contracts")
    model = Contract
    template_name = "contracts/confirm_delete_contract.html"


class ContractParseView(View):

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        cores = ContractCore.objects.filter(contract=contract)
        # TODO: lepší rozlišování smluv
        template = "contracts/mustr_template.html"
        context = {
            "contract": contract,
            "cores": cores,
        }
        return TemplateResponse(request, template, context)


class ContractsTableView(SingleTableMixin, FilterView):
    table_class = ContractTable
    model = Contract
    template_name = "contracts/dashboard.html"
    filterset_class = ContractFilter


class ContractCoresEditView(View):

    def get(self, request, pk, *args, **kwargs):
        contract = Contract.objects.get(id=pk)
        cores = contract.contract_cores.all()
        context = {
            "contract": contract,
            "cores": cores,
        }
        return TemplateResponse(template="contracts/edit_cores.html", request=request, context=context)

    def post(self, request, pk, *args, **kwargs):
        data = request.POST
        contract = Contract.objects.get(id=pk)
        for id, text in data.items():
            if id.isnumeric():
                old_core = ContractCore.objects.get(id=id)
                if old_core.text != text:
                    # same in database
                    match = ContractCore.objects.filter(text=text) # redis?
                    if match.count() == 1:
                        contract.contract_cores.set(match)
                        contract.contract_cores.remove(old_core)
                    # TODO: implementovat sentry
                    # elif match.count() > 1:
                    #     print("pošli to do sentry")
                    else:
                        # make new core
                        new_core = ContractCore.objects.create(
                            text=text,
                            priority=old_core.priority,
                            essential=old_core.essential,
                            editable=old_core.editable,
                            parent_id=old_core.id,
                            default=False,
                        )
                        new_core.contract_type.add(old_core.contract_type.get()) # how to add in create method?
                        contract.contract_cores.add(new_core)
                        contract.contract_cores.remove(old_core)

        return redirect('edit-contract', contract.id)


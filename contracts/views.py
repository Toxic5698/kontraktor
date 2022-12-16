from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from proposals.models import Proposal
from contracts.constants import CONTRACT_SECTIONS
from contracts.forms import ContractForm
from contracts.models import Contract, ContractCore
from contracts.tables import ContractTable
from contracts.filters import ContractFilter


class ContractCreateView(View):
    def post(self, request, proposal_id, *args, **kwargs):
        # TODO: zkontrolovat všechny údaje než se smlova vytvoří a poslat zprávu o chybějících
        proposal = Proposal.objects.get(id=proposal_id)
        contract = Contract.objects.create(
            proposal=proposal,
            contract_number=proposal.proposal_number,
            client=proposal.client
        )
        return redirect("edit-contract", contract.id)


class ContractUpdateView(UpdateView):
    form_class = ContractForm
    template_name = "contracts/edit_contract.html"
    model = Contract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edited_cores'] = ContractCore.objects.filter(default=False, contract=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy("manage-attachments", args=(self.get_object().id,))


class ContractDeleteView(DeleteView):
    success_url = reverse_lazy("contracts")
    model = Contract
    template_name = "contracts/confirm_delete_contract.html"


class ContractParseView(View):

    def get(self, request, pk):
        contract = Contract.objects.prefetch_related('contract_cores').get(id=pk)
        template = "contracts/contract_mustr.html"
        context = {
            "contract": contract,
            "sections": CONTRACT_SECTIONS
        }
        for index, section in enumerate(CONTRACT_SECTIONS, 1):
            cores = contract.contract_cores.filter(section=section[0])
            if cores.count() > 0:
                context["cores_" + str(index)] = cores

        return TemplateResponse(request, template, context)


class ContractsTableView(SingleTableMixin, FilterView):
    table_class = ContractTable
    model = Contract
    template_name = "contracts/contract_list.html"
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


class ContractSendView(UpdateView):
    model = Contract


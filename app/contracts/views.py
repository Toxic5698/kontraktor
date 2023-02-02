from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from operators.models import Operator
from proposals.forms import ProposalEditForm
from proposals.models import Proposal
from contracts.forms import ContractForm
from contracts.models import Contract, ContractCore
from contracts.tables import ContractTable
from contracts.filters import ContractFilter


class ContractCreateView(LoginRequiredMixin, View):
    def post(self, request, proposal_id, *args, **kwargs):
        # TODO: zkontrolovat všechny údaje než se smlova vytvoří a poslat zprávu o chybějících
        proposal = Proposal.objects.get(id=proposal_id)
        contract = Contract.objects.create(
            proposal=proposal,
            contract_number=proposal.proposal_number,
            client=proposal.client,
            created_by=request.user,
        )
        return redirect("edit-contract", contract.id)


class ContractUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        contract = Contract.objects.get(pk=pk)
        proposal = contract.proposal
        contract_form = ContractForm(instance=contract)
        proposal_form = ProposalEditForm(instance=contract.proposal)
        context = {
            "contract": contract,
            "proposal": proposal,
            "contract_form": contract_form,
            "proposal_form": proposal_form,
            "operator": Operator.objects.get()
        }
        return TemplateResponse(request=request, template="contracts/../templates/contracts/edit_contract.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        contract = Contract.objects.get(pk=pk)
        proposal = contract.proposal

        if "contract" in request.POST:
            contract_form = ContractForm(request.POST, instance=contract)
            if contract_form.is_valid():
                contract_form.save()
                contract.edited_by = request.user
                contract.save()
        if "proposal" in request.POST:
            proposal_form = ProposalEditForm(request.POST, instance=proposal)
            if proposal_form.is_valid():
                proposal_form.save()
                proposal.edited_by = request.user
                proposal.save()

        return redirect("edit-contract", contract.id)


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("contracts")
    model = Contract
    template_name = "contracts/../templates/contracts/confirm_delete_contract.html"


class ContractsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ContractTable
    model = Contract
    template_name = "contracts/../templates/contracts/contract_list.html"
    filterset_class = ContractFilter


class ContractCoresEditView(LoginRequiredMixin, View):

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
                    match = ContractCore.objects.filter(text=text)  # redis?
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
                        new_core.contract_type.add(old_core.contract_type.get())  # how to add in create method?
                        contract.contract_cores.add(new_core)
                        contract.contract_cores.remove(old_core)

        return redirect('edit-contract', contract.id)


class ContractSendView(LoginRequiredMixin, UpdateView):
    model = Contract

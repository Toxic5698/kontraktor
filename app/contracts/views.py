from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from attachments.forms import AttachmentUploadForm
from base.methods import get_data_in_dict
from clients.models import Client
from emailing.models import Mail
from emailing.services import send_email_service
from operators.models import Operator
from proposals.forms import ProposalEditForm
from proposals.models import Proposal, Item
from contracts.forms import ContractForm
from contracts.models import Contract, ContractCore, Protocol, ProtocolItem
from contracts.tables import ContractTable
from contracts.filters import ContractFilter


class ContractCreateView(LoginRequiredMixin, View):
    def post(self, request, proposal_id, *args, **kwargs):
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
        return TemplateResponse(request=request, template="contracts/edit_contract.html", context=context)

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
    template_name = "contracts/confirm_delete_contract.html"


class ContractsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ContractTable
    model = Contract
    template_name = "contracts/contract_list.html"
    filterset_class = ContractFilter


class ContractCoresEditView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        contract = Contract.objects.get(id=pk)
        context = {
            "contract": contract,
            "cores": contract.contract_cores.all().order_by("contract_section__priority", "priority"),
            "sections": contract.proposal.contract_type.contract_sections.all(),
        }
        return TemplateResponse(template="contracts/edit_cores.html", request=request, context=context)

    def post(self, request, pk, *args, **kwargs):
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        contract = Contract.objects.get(id=pk)
        if "save_changes" in data.keys():
            data.pop("save_changes")
            for id, text in data.items():
                if id.isnumeric():
                    old_core = ContractCore.objects.get(id=id)
                    if old_core.editable and old_core.text != text.strip("\r\n "):
                        # same in database
                        match = ContractCore.objects.filter(text=text.strip("\r\n "))  # redis?
                        if match.count() == 1:
                            contract.contract_cores.add(match.get())
                            contract.contract_cores.remove(old_core)
                        elif match.count() > 1:
                            messages.warning(request, "Nalezeno více shodných ustanovení, kontaktujte správce systému.")
                        else:
                            # make new core
                            new_core = ContractCore.objects.create(
                                text=text.strip("\r\n "),
                                contract_section=old_core.contract_section,
                                priority=old_core.priority,
                                essential=old_core.essential,
                                editable=old_core.editable,
                                parent_id=old_core.id,
                                default=False,
                            )
                            new_core.contract_type.add(old_core.contract_type.get())  # how to add in create method?
                            contract.contract_cores.add(new_core)
                            contract.contract_cores.remove(old_core)
        elif "save_new" in data.keys():
            data.pop("save_new")
            new_core = ContractCore.objects.create(
                text=data.get("text").strip("\r\n "),
                contract_section_id=data.get("section"),
                priority=int(data.get("priority")),
                essential=False,
                editable=True,
                default=False,
            )
            contract.contract_cores.add(new_core)
        elif "remove_core" in data.keys():
            core = ContractCore.objects.get(id=data.get("remove_core"))
            contract.contract_cores.remove(core)

        return redirect('edit-cores', contract.id)


class ContractSendView(LoginRequiredMixin, View):
    def post(self, request, pk=None, *args, **kwargs):
        contract = Contract.objects.get(pk=pk)
        send_email_service(
            subject=f"new_contract {contract.contract_number}",
            client=contract.client,
            sender = request.user,
            link = request.META['HTTP_HOST']
        )
        messages.warning(request, "Smlouva byla klientovi odeslána.")

        return redirect("edit-contract", contract.id)


class ProtocolCreateView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        client = Client.objects.get(pk=pk)
        contracts = Contract.objects.filter(client=client).select_related("proposal")
        form = AttachmentUploadForm()
        context = {
            "client": client,
            "contracts": contracts,
            "form": form,
        }
        return TemplateResponse(template="contracts/create_protocol.html", request=request, context=context)

    def post(self, request, pk, *args, **kwargs):
        data = get_data_in_dict(request)
        protocol_note = data.pop('protocol_note')
        contract_id = data.pop('contract_id')
        protocol = Protocol.objects.create(
            contract_id=contract_id,
            client=Client.objects.get(pk=pk),
            created_by=request.user,
            note=f"{timezone.now().strftime('%d. %m. %Y %H:%M')} - {protocol_note}"

        )

        reference_date = timezone.now().date()
        statuses = {}
        notes = {}
        descs = {}
        for key, value in data.items():
            prefix, counter, id = key.split("_")
            if "handedover" in prefix:
                statuses[counter] = [id, value]
            if "itemnote" in prefix and value != "":
                notes[counter] = value
            if "desc" in prefix and value != "":
                descs[counter] = value
        for key, value in statuses.items():
            ProtocolItem.objects.create(
                protocol=protocol,
                item=Item.objects.get(id=value[0]),
                created_by=request.user,
                created_at=reference_date,
                status=value[1],
                note=notes.get(key),
                description=descs.get(key)
            )
        messages.success(request, "Protokol uložen.")
        return redirect("manage-attachments", protocol.contract.client.id)

class ProtocolEditView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        protocol = Protocol.objects.get(pk=pk)
        form = AttachmentUploadForm()
        context = {
            "protocol" : protocol,
            "items": protocol.items.all(),
            "client": protocol.contract.client,
            "form": form,
        }
        return TemplateResponse(request=request, template="contracts/edit_protocol.html", context=context)

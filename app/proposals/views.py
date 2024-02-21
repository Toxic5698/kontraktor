from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from attachments.models import DefaultAttachment
from clients.forms import ClientForm
from clients.models import Client
from operators.models import Operator
from proposals.enums import UnitOptions
from proposals.forms import ProposalUploadForm, ProposalEditForm
from proposals.models import Proposal, UploadedProposal, Item, check_payments, ContractSubject, DefaultItem, \
    ContractType
from proposals.peli_parser import parse_items
from proposals.filters import ProposalFilter
from proposals.tables import ProposalTable


class ProposalsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ProposalTable
    model = Proposal
    template_name = "proposals/proposals_list.html"
    filterset_class = ProposalFilter


class ProposalEditView(LoginRequiredMixin, View):

    def get(self, request, pk=None, client_id=None, *args, **kwargs):
        context = {}
        if pk:
            proposal = Proposal.objects.get(pk=pk)
            context["proposal"] = proposal
            edit_form = ProposalEditForm(instance=proposal)
        elif client_id:
            client = Client.objects.get(pk=client_id)
            context["client"] = client
            edit_form = ProposalEditForm(initial={"client": client})
        else:
            edit_form = ProposalEditForm()
            client_form = ClientForm()
            context["client_form"] = client_form

        upload_form = ProposalUploadForm()
        context["upload_form"] = upload_form
        context["edit_form"] = edit_form
        context["uploaded"] = UploadedProposal.objects.last()

        return TemplateResponse(template="proposals/edit_proposal.html", request=request, context=context)

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            proposal = Proposal.objects.get(pk=pk)
            form = ProposalEditForm(request.POST, instance=proposal)
            if form.is_valid():
                form.save()
                proposal.edited_by = request.user
                proposal.save()
        else:
            data = request.POST.dict()
            if "client" in data.keys():
                client = Client.objects.get(pk=data["client"])
            else:
                client = Client.objects.create(
                    name=data["name"],
                    email=data["email"],
                    id_number=data["id_number"],
                    address=data["address"],
                    phone_number=data["phone_number"],
                    note=data["note"],
                    consumer=True if data["consumer"] == "on" else False,
                )

            if Proposal.objects.filter(proposal_number=data["proposal_number"]).count() > 0:
                messages.warning(request, "Nabídka s tímto číslem již existuje!")
                return redirect("edit-proposal")
            proposal = Proposal.objects.create(
                client=client,
                proposal_number=data["proposal_number"],
                subject=ContractSubject.objects.get(id=data["subject"]),
                contract_type=ContractType.objects.get(id=data["contract_type"]),
                fulfillment_at=data["fulfillment_at"],
                fulfillment_place=data["fulfillment_place"],
                created_by=request.user,
            )
            default_items = DefaultItem.objects.filter(subject=proposal.subject, contract_type=proposal.contract_type)
            if default_items.exists():
                for item in default_items:
                    Item.objects.create(
                        proposal=proposal,
                        quantity=1,
                        title=item.title,
                        description=item.description,
                        production_price=item.production_price,
                        price_per_unit=item.price_per_unit,
                        unit=item.unit,
                    )
            default_attachments = DefaultAttachment.objects.filter(subject=proposal.subject, contract_type=proposal.contract_type)
            if default_attachments.exists():
                for attachment in default_attachments:
                    client.default_attachments.add(attachment)

        if len(request.FILES) > 0 and "proposal" in locals():
            file = request.FILES["file"]
            parse_result = parse_items(file, proposal)
            if parse_result == "success":
                UploadedProposal.objects.create(
                    file=file,
                    file_name=file.name,
                    proposal=proposal,
                )
            else:
                messages.warning(request, parse_result)

        return redirect('edit-proposal', proposal.id)


class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    model = Proposal
    template_name = 'proposals/confirm_delete_proposal.html'
    success_url = reverse_lazy("proposals")


class ProposalItemsView(LoginRequiredMixin, View):

    def get(self, request, pk=None, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        context = {
            "proposal": proposal,
            "units": UnitOptions,
        }
        return TemplateResponse(template="proposals/edit_items.html", context=context, request=request)

    def post(self, request, pk, *args, **kwargs):
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        if "create" in request.POST:
            data.pop("create")
            proposal = Proposal.objects.get(pk=pk)
            Item.objects.create(
                proposal=proposal,
                **data
            )
        else:
            item = Item.objects.get(pk=pk)
            proposal = item.proposal
            if "delete" in request.POST:
                item.delete()
            if "save" in request.POST:
                data.pop("save")
                item.save(**data)

        return redirect('edit-items', proposal.id)


class PaymentsEditView(LoginRequiredMixin, View):

    def post(self, request, proposal_id, *args, **kwargs):
        proposal = Proposal.objects.get(pk=proposal_id)
        for index, payment in enumerate(proposal.payments.all()):
            payment.part = request.POST.getlist("payment_part")[index]
            payment.due = request.POST.getlist("payment_due")[index]
            success = payment.save()
            if not success:
                messages.warning(request, "U plateb musí být nastavena splatnost.")
        if not check_payments(proposal):
            messages.warning(request, "Souhrn částí plateb se nerovná celku.")
        return redirect(request.META.get('HTTP_REFERER'))

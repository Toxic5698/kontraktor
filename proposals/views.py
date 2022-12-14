from decimal import Decimal

from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, FormView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from clients.forms import ClientForm
from clients.models import Client
from contracts.models import ContractType
from proposals.forms import ProposalUploadForm, ProposalEditForm
from proposals.models import Proposal, UploadedProposal, Item, check_payments
from proposals.peli_parser import parse_items
from proposals.filters import ProposalFilter
from proposals.tables import ProposalTable


class ProposalsTableView(SingleTableMixin, FilterView):
    table_class = ProposalTable
    model = Proposal
    template_name = "proposals/proposals_list.html"
    filterset_class = ProposalFilter


class ProposalEditView(View):

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
                raise ValueError("Nab??dka s t??mto ????slem ji?? existuje!")
            proposal = Proposal.objects.create(
                client=client,
                proposal_number=data["proposal_number"],
                subject=data["subject"],
                contract_type=ContractType.objects.get(id=data["contract_type"]),
                # TODO: o??et??it datumy
                # fulfillment_at=data["fulfillment_at"],
                fulfillment_place=data["fulfillment_place"],
            )

        if len(request.FILES) > 0:
            file = request.FILES["file"]
            UploadedProposal.objects.create(
                file=file,
                file_name=file.name,
                proposal=proposal,
            )
            parse_result = parse_items(file, proposal)

        return redirect('edit-proposal', proposal.id)


class ProposalDeleteView(DeleteView):
    model = Proposal
    template_name = 'proposals/confirm_delete_proposal.html'
    success_url = reverse_lazy("proposals")


class ProposalItemsView(View):

    def get(self, request, pk=None, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        context = {
            "proposal": proposal,
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


class ProposalGenerateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        context = {
            "proposal": proposal,
        }
        return TemplateResponse(template="proposals/proposal_mustr.html", context=context, request=request)


class ProposalSendView(View):
    def get(self, request, pk=None, *args, **kwargs):
        context = {}
        return TemplateResponse(template="proposals/send_proposal.html", context=context, request=request)


class PaymentsEditView(View):

    def post(self, request, proposal_id, *args, **kwargs):
        proposal = Proposal.objects.get(pk=proposal_id)
        for index, payment in enumerate(proposal.payments.all()):
            payment.part = request.POST.getlist("payment_part")[index]
            payment.due = request.POST.getlist("payment_due")[index]
            payment.save()
        check_payments(proposal)
        return redirect(request.META.get('HTTP_REFERER'))

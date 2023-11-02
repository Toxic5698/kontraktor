from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from clients.forms import ClientForm
from clients.models import Client
from contracts.models import ContractType, Contract, ProtocolItem
from emailing.models import Mail
from operators.models import Operator
from proposals.forms import ProposalUploadForm, ProposalEditForm
from proposals.models import Proposal, UploadedProposal, Item, check_payments, ContractSubject, DefaultItem
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


class ProtocolItemListView(View):

    def get(self, request, *args, **kwargs):
        protocol_items = []
        for item in Item.objects.filter(proposal_id=request.GET.get("pk")):
            protocol_item = {
                "id": item.id,
                "title": item.title,
            }
            handed_over = ProtocolItem.objects.filter(item=item, status="yes").count()
            protocol_items.extend(protocol_item for x in range(item.quantity - handed_over))
        contract = Contract.objects.get(proposal_id=request.GET.get("pk"))
        context = {"items": protocol_items, "contract": contract}
        return TemplateResponse(request, "contracts/protocol_items.html", context)


class ProposalSendView(LoginRequiredMixin, View):
    def post(self, request, pk=None, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        Mail.objects.create(
            subject=f"Nabídka od společnosti {Operator.objects.get()}",
            message=f"Nabídku naleznete na tomto odkazu: {request.META['HTTP_HOST']}/clients/{proposal.client.sign_code}",
            recipients=proposal.client.email,
            client=proposal.client
        )
        messages.warning(request, "Nabídka byla klientovi odeslána.")

        return redirect("edit-proposal", proposal.id)


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

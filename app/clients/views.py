import base64
import io
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from easy_pdf.views import PDFTemplateView
from ipware import get_client_ip

from clients.filters import ClientFilter
from clients.forms import ClientForm
from clients.models import Client, Signature
from clients.tables import ClientTable
from contracts.models import ContractSection
from emailing.models import Mail
from operators.models import Operator


class ClientsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ClientTable
    model = Client
    template_name = "clients/clients_list.html"
    filterset_class = ClientFilter


class ClientCreateView(LoginRequiredMixin, CreateView):
    form_class = ClientForm
    template_name = "clients/edit_client.html"
    model = Client

    def get_success_url(self):
        return reverse_lazy("edit-client", args=(self.object.id,))


class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = "clients/edit_client.html"
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy("edit-client", args=(self.get_object().id,))


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("clients")
    model = Client
    template_name = "clients/confirm_delete_client.html"


class DocumentsToSignView(View):

    def get(self, request, sign_code, *args, **kwargs):
        client = Client.objects.get(sign_code=sign_code)
        documents = self.get_documents(client)
        context = {
            "client": client,
            "documents": documents,
        }
        return TemplateResponse(template="clients/list_to_sign.html", request=request, context=context)

    def get_documents(self, client):
        documents = []
        proposals = client.proposals.all()
        for proposal in proposals:
            document = {
                "id": proposal.id,
                "type": "proposal",
                "title": f"Nabídka č. {proposal.proposal_number}",
                "price": proposal.price_brutto,
                "attachments": client.attachments.filter_proposals(),
                "attachments_count": client.attachments.filter_proposals().count(),
                "signed": True if proposal.signed_at else False,
                "last_update": proposal.edited_at.strftime('%d. %m. %Y'),
                "items_count": proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = proposal.signed_at.strftime('%d. %m. %Y')
            documents.append(document)

        contracts = client.contracts.all()
        for contract in contracts:
            document = {
                "id": contract.id,
                "type": "contract",
                "title": f"Smlouva č. {contract.contract_number}",
                "price": contract.proposal.price_brutto,
                "attachments": client.attachments.filter_contracts(),
                "attachments_count": client.attachments.filter_contracts().count(),
                "signed": True if contract.signed_at else False,
                "last_update": contract.edited_at.strftime('%d. %m. %Y'),
                "items_count": contract.proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = contract.signed_at.strftime('%d. %m. %Y')
            documents.append(document)
        return documents


class SigningDocument(View):

    def get(self, request, *args, **kwargs):
        model = apps.get_model(model_name=self.kwargs["type"], app_label=(self.kwargs["type"] + "s"))
        document = model.objects.get(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        if document.signed_at:
            return redirect("document-to-sign", document.client.sign_code)
        context = {"document": document}
        return TemplateResponse(template="clients/signing_document.html", context=context, request=request)

    def post(self, request, *args, **kwargs):
        model = apps.get_model(model_name=self.kwargs["type"], app_label=(self.kwargs["type"] + "s"))
        document = model.objects.get(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        file = request.FILES.get("file")
        ip, is_routable = get_client_ip(request)
        Signature.objects.create(
            client=document.client,
            file=file,
            document_object=document,
            ip=ip,
        )

        document.signed_at = timezone.now()
        document.save()

        return HttpResponse("OK", status=200)


class DocumentView(PDFTemplateView):

    def get_queryset(self):
        model = apps.get_model(model_name=self.kwargs["type"], app_label=(self.kwargs["type"] + "s"))
        queryset = model.objects.filter(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        return queryset

    def get_template_names(self):
        template = f"{self.kwargs['type'] + 's'}/{self.kwargs['type']}_mustr.html"
        return [template, ]

    def get_context_data(self, **kwargs):
        context = {
            "operator": Operator.objects.get(),
        }
        if self.kwargs["type"] == "contract":
            contract = self.get_queryset().get()
            context["contract"] = contract
            context["proposal"] = contract.proposal
            cores = contract.contract_cores.all()

            sections = {}
            for section in ContractSection.objects.filter(contract_cores__in=cores).distinct():
                sections[section.name] = cores.filter(contract_section=section).values_list("text", flat=True)
            context["sections"] = sections

            if contract.client.signatures.exists() and contract.signed_at:
                context["signature"] = contract.client.signatures.filter(contract=contract).last()

        if self.kwargs["type"] == "proposal":
            proposal = self.get_queryset().get()
            context["proposal"] = proposal
            context["proposal_validity"] = proposal.edited_at + timedelta(days=14)
            context["production_data"] = proposal.items.filter(production_data__isnull=False)

        return context

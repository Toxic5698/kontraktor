import base64
import io
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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

from attachments.serializers import attachments_serializer
from clients.filters import ClientFilter
from clients.forms import ClientForm
from clients.models import Client, Signature
from clients.services import create_demo_client
from clients.tables import ClientTable
from contracts.models import ContractSection
from emailing.services import send_email_service
from operators.models import Operator


class ClientsTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ClientTable
    model = Client
    template_name = "clients/clients_list.html"
    filterset_class = ClientFilter
    ordering = "-id"


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

        # proposals
        proposals = client.proposals.all()
        all_proposal_attachments = attachments_serializer(
            client.attachments.filter_proposals()) + attachments_serializer(
            client.default_attachments.filter_proposals())
        for proposal in proposals:
            document = {
                "id": proposal.id,
                "type": "proposal",
                "title": f"Nabídka č. {proposal.proposal_number}",
                "price": proposal.price_brutto,
                "attachments": all_proposal_attachments,
                "attachments_count": len(all_proposal_attachments),
                "signed": True if proposal.signed_at else False,
                "last_update": proposal.edited_at.strftime('%d. %m. %Y'),
                "items_count": proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = proposal.signed_at.strftime('%d. %m. %Y')
            documents.append(document)

        # contracts
        contracts = client.contracts.all()
        all_contract_attachments = attachments_serializer(
            client.attachments.filter_contracts()) + attachments_serializer(
            client.default_attachments.filter_contracts())
        for contract in contracts:
            document = {
                "id": contract.id,
                "type": "contract",
                "title": f"Smlouva č. {contract.contract_number}",
                "price": contract.proposal.price_brutto,
                "attachments": all_contract_attachments,
                "attachments_count": len(all_contract_attachments),
                "signed": True if contract.signed_at else False,
                "last_update": contract.edited_at.strftime('%d. %m. %Y'),
                "items_count": contract.proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = contract.signed_at.strftime('%d. %m. %Y')
            documents.append(document)

        # protocols
        protocols = client.protocols.all()
        all_protocol_attachments = attachments_serializer(
            client.attachments.filter_protocols()) + attachments_serializer(
            client.default_attachments.filter_protocols())
        for protocol in protocols:
            document = {
                "id": protocol.id,
                "type": "protocol",
                "title": f"Předávací protokol ke smlouvě č. {protocol.contract.contract_number}",
                "attachments": all_protocol_attachments,
                "attachments_count": len(all_protocol_attachments),
                "signed": True if protocol.signed_at else False,
                "last_update": protocol.created_at.strftime('%d. %m. %Y'),
            }
            if document["signed"]:
                document["signed_at"] = protocol.signed_at.strftime('%d. %m. %Y')
            documents.append(document)
        return documents


class SigningDocument(View):

    def get(self, request, *args, **kwargs):
        model = get_document_model(self.kwargs["type"])
        document = model.objects.get(pk=self.kwargs['pk'], client__sign_code=self.kwargs['sign_code'])
        if document.signed_at:
            return redirect("document-to-sign", document.client.sign_code)
        context = {"document": document}
        return TemplateResponse(template="clients/signing_document.html", context=context, request=request)

    def post(self, request, *args, **kwargs):
        model = get_document_model(self.kwargs["type"])
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

        document_type = model.__name__.lower()
        if document_type == "proposal":
            number = document.proposal_number
        elif document_type == "contract":
            number = document.contract_number
        else:
            number = document.contract.contract_number

        send_email_service(
            subject=f"signed_{document_type} {number}",
            client=document.client,
            link=request.META['HTTP_HOST']
        )

        return HttpResponse("OK", status=200)


class DocumentView(PDFTemplateView):

    def get_queryset(self):
        model = get_document_model(self.kwargs["type"])
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
            context["attachments"] = attachments_serializer(
                contract.client.attachments.filter_contracts()) + attachments_serializer(
                contract.client.default_attachments.filter_contracts())
            cores = contract.contract_cores.filter(Q(subject__isnull=True) | Q(subject=contract.proposal.subject))

            sections = {}
            for section in ContractSection.objects.filter(contract_cores__in=cores).distinct().order_by('priority'):
                sections[section.name] = cores.filter(contract_section=section).values_list("text", flat=True)
            context["sections"] = sections

            if contract.client.signatures.exists() and contract.signed_at:
                context["signature"] = contract.client.signatures.filter(contract=contract).last()

        if self.kwargs["type"] == "proposal":
            proposal = self.get_queryset().get()
            context["proposal"] = proposal
            context["proposal_validity"] = proposal.edited_at + timedelta(days=14)
            context["production_data"] = proposal.items.filter(production_data__isnull=False)
            context["attachments"] = attachments_serializer(
                proposal.client.attachments.filter_proposals()) + attachments_serializer(
                proposal.client.default_attachments.filter_contracts())

        if self.kwargs["type"] == "protocol":
            protocol = self.get_queryset().get()
            context["protocol"] = protocol
            context["proposal"] = protocol.contract.proposal
            context["attachments"] = attachments_serializer(
                protocol.client.attachments.filter_protocols()) + attachments_serializer(
                protocol.client.default_attachments.filter_protocols())

            if protocol.client.signatures.exists() and protocol.signed_at:
                context["signature"] = protocol.client.signatures.filter(protocol=protocol).last()

        return context


def get_document_model(doc_type):
    if doc_type == "proposal":
        app_label = "proposals"
    else:
        app_label = "contracts"
    model = apps.get_model(model_name=doc_type, app_label=app_label)
    return model


class CreateDemoClient(View):

    def get(self, request, *args, **kwargs):
        sign_code = create_demo_client()
        return redirect("document-to-sign", sign_code)


class SignTestView(View):

    def get(self, request, pk, *args, **kwargs):
        context = {
            "signature": Signature.objects.get(id=pk)
        }
        return TemplateResponse(request, "document_components/signs.html", context)

from datetime import timedelta

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from ipware import get_client_ip

from attachments.serializers import attachments_serializer
from clients.filters import ClientFilter
from clients.forms import ClientForm
from clients.models import Client, Signature
from clients.services import create_demo_client
from clients.tables import ClientTable
# from contracts.models import ContractSection
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
        for proposal in proposals:
            document = {
                "id": proposal.id,
                "type": "proposal",
                "title": proposal.get_name(),
                "price": proposal.price_brutto,
                "attachments": proposal.attachments.all(),
                "attachments_count": proposal.attachments.all().count(),
                "signed": True if proposal.signed_at else False,
                "last_update": proposal.edited_at.strftime('%d. %m. %Y'),
                "items_count": proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = proposal.signed_at.strftime('%d. %m. %Y')
            documents.append(document)

        # contracts
        contracts = client.contracts.all()
        # all_contract_attachments = attachments_serializer(
        #     client.attachments.filter_contracts()) + attachments_serializer(
        #     client.default_attachments.filter_contracts())
        for contract in contracts:
            document = {
                "id": contract.id,
                "type": "contract",
                "title": f"Smlouva č. {contract.document_number}",
                "price": contract.proposal.price_brutto,
                "attachments": contract.attachments.all(),
                "attachments_count": contract.attachments.all().count(),
                "signed": True if contract.signed_at else False,
                "last_update": contract.edited_at.strftime('%d. %m. %Y'),
                "items_count": contract.proposal.items.all().count(),
            }
            if document["signed"]:
                document["signed_at"] = contract.signed_at.strftime('%d. %m. %Y')
            documents.append(document)

        # protocols
        protocols = client.protocols.all()
        # all_protocol_attachments = attachments_serializer(
        #     client.attachments.filter_protocols()) + attachments_serializer(
        #     client.default_attachments.filter_protocols())
        for protocol in protocols:
            document = {
                "id": protocol.id,
                "type": "protocol",
                "title": f"Předávací protokol ke smlouvě č. {protocol.contract.document_number}",
                "attachments": protocol.attachments.all(),
                "attachments_count": protocol.attachments.all().count(),
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

        link = "http://" + request.META['HTTP_HOST'] + "/clients/" + str(document.client.sign_code)
        send_email_service(document=document, link=link)

        return HttpResponse("OK", status=200)


def get_document_model(doc_type):
    if doc_type == "proposal":
        app_label = "proposals"
    else:
        app_label = "contracts"
    model = apps.get_model(model_name=doc_type, app_label=app_label)
    return model


class CreateDemoClient(View):

    def get(self, request, *args, **kwargs):
        host = request.META["HTTP_HOST"]
        if "localhost" in host or "demo" in host or "devel" in host:
            sign_code = create_demo_client()
            return redirect("document-to-sign", sign_code)

        else:
            messages.warning(request, "Automatické vytváření klientů není v této instanci možné.")
            return redirect("welcome-page")

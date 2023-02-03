import functools
import ssl

from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import UpdateView, DeleteView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.utils import django_url_fetcher
from django_weasyprint.views import WeasyTemplateResponse

from clients.filters import ClientFilter
from clients.forms import ClientForm
from clients.models import Client
from clients.tables import ClientTable
from contracts.constants import CONTRACT_SECTIONS
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
                "price": proposal.price,
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
                "price": contract.proposal.price,
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
        context = {"document": document}
        return TemplateResponse(template="clients/signing_document.html", context=context, request=request)

    def post(self, request, *args, **kwargs):
        document = self.get(request, *args, **kwargs)
        return reverse_lazy("document-to-sign", document.client.sing_code)


class MyDetailView(DetailView):

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
            context["sections"] = CONTRACT_SECTIONS

            for index, section in enumerate(CONTRACT_SECTIONS, 1):
                cores = contract.contract_cores.filter(section=section[0])
                if cores.count() > 0:
                    context["cores_" + str(index)] = cores

        if self.kwargs["type"] == "proposal":
            context["proposal"] = self.get_queryset().get()

        return context


def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    storage_url = 'http://127.0.0.1:8099/'
    if url.startswith(storage_url):
        url = 'file://' + url.replace(storage_url, settings.STATIC_URL)
    return django_url_fetcher(url, *args, **kwargs)


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to pass a kwarg to URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(custom_url_fetcher, ssl_context=context)


class PrintView(WeasyTemplateResponseMixin, MyDetailView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    # pdf_stylesheets = [
    #     settings.STATIC_ROOT + 'css/css',
    # ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, MyDetailView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'


class DynamicDocumentView(WeasyTemplateResponseMixin, MyDetailView):

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )

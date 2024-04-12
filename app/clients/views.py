from django.contrib import messages
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
from ipware import get_client_ip

from base.methods import get_documents_for_client, get_model
from clients.filters import ClientFilter
from clients.forms import ClientForm
from clients.models import Client, Signature
from clients.services import create_demo_client
from clients.tables import ClientTable
from emailing.services import send_email_service


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
        client, documents = get_documents_for_client(sign_code=sign_code)
        context = {
            "client": client,
            "documents": documents,
        }
        return TemplateResponse(template="clients/list_to_sign.html", request=request, context=context)


class SigningDocument(View):

    def get(self, request, *args, **kwargs):
        model = get_model(self.kwargs["type"])
        document = model.objects.get(pk=self.kwargs["pk"], client__sign_code=self.kwargs["sign_code"])
        if document.signed_at:
            return redirect("document-to-sign", document.client.sign_code)
        context = {"document": document}
        return TemplateResponse(template="clients/signing_document.html", context=context, request=request)

    def post(self, request, *args, **kwargs):
        model = get_model(self.kwargs["type"])
        document = model.objects.get(pk=self.kwargs["pk"], client__sign_code=self.kwargs["sign_code"])
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

        link = "http://" + request.META["HTTP_HOST"] + "/clients/" + str(document.client.sign_code)
        send_email_service(document=document, link=link)

        return HttpResponse("OK", status=200)


class CreateDemoClient(View):

    def get(self, request, *args, **kwargs):
        host = request.META["HTTP_HOST"]
        if "localhost" in host or "demo" in host or "devel" in host:
            sign_code = create_demo_client()
            return redirect("document-to-sign", sign_code)

        else:
            messages.warning(request, "Automatické vytváření klientů není v této instanci možné.")
            return redirect("welcome-page")

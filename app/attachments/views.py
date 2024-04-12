from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView

from attachments.models import Attachment
from base.methods import get_data_in_dict, get_model, get_documents_for_client
from clients.models import Client


class AttachmentManageView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        client = Client.objects.prefetch_related("protocols").get(pk=pk)
        context = {
            "client": client,
            "protocols": client.protocols.all(),
        }
        return TemplateResponse(request=request, template="attachments/manage_attachments.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        client = Client.objects.get(pk=pk)
        if len(request.FILES) > 0:
            files = request.FILES.getlist("file")
            for file in files:
                Attachment.objects.create(client=client, file=file, file_name=file.name)
        return redirect("manage-attachments", client.id)


class AttachmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Attachment
    template_name = "attachments/confirm_delete_attachment.html"

    def get_success_url(self):
        return reverse_lazy("manage-attachments", args=(self.get_object().client_id,))


class UploadedAttachmentView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        client, documents = get_documents_for_client(client_id=pk)
        context = {
            "client": client,
            "documents": documents,
        }
        return TemplateResponse(request=request, template="attachments/uploaded_attachments.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        attachment = Attachment.objects.get(pk=pk)
        data = get_data_in_dict(request)
        if attachment.is_intern() and data.get("intern"):
            data.pop("intern")
        if data.get("attachment_tag"):
            attachment.tag = data["attachment_tag"]
        elif data.get("intern") or len(data) == 0:
            attachment.change_to_intern("intern")
        elif "add" in data.values():
            for document in data.keys():
                model_name, doc_id = document.split(".")
                model = get_model(model_name=model_name)
                model.objects.get(id=doc_id).attachments.add(attachment)

        attachment.save()
        return HttpResponse(f"Attachment attribute saved.")


class DefaultAttachmentView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        client, documents = get_documents_for_client(client_id=pk)
        default_attachments = []
        for document in documents:
            for attachment in document.default_attachments.all():
                default_attachments.append(attachment)
        context = {
            "client": client,
            "documents": documents,
            "default_attachments": default_attachments,
        }
        return TemplateResponse(request=request, template="attachments/default_attachments.html", context=context)

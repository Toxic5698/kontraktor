from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView

from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from base.methods import get_data_in_dict
from clients.models import Client
from contracts.models import Protocol, Contract
from proposals.models import Proposal


class AttachmentManageView(LoginRequiredMixin, View):
    # form_class = AttachmentUploadForm

    def get(self, request, pk, *args, **kwargs):
        client = Client.objects.prefetch_related("proposals", "contracts", "protocols").get(pk=pk)
        documents = []
        for proposal in client.proposals.all():
            documents.append(proposal)
        for contract in client.contracts.all():
            documents.append(contract)
        for protocol in client.protocols.all():
            documents.append(protocol)
        context = {"client": client,
                   "documents": documents,
                   "protocols": client.protocols.all(),
                   "proposals": client.proposals.all(),
                   "contracts": client.contracts.all()}
        return TemplateResponse(request=request, template="attachments/manage_attachments.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        if len(request.FILES) > 0:
            client = Client.objects.get(pk=pk)
            files = request.FILES.getlist('file')
            for file in files:
                Attachment.objects.create(
                    client=client,
                    file=file,
                    file_name=file.name
                )
        else:
            attachment = Attachment.objects.get(pk=pk)
            client = attachment.client
            data = get_data_in_dict(request)
            if data.get("attachment_tag"):
                attachment.tag = data["attachment_tag"]
            elif data.get("intern") or len(data) == 0:
                attachment.purpose = data["intern"]
            elif "add" in data.values():
                attachment.purpose = data.get("add")

            # attachment.save()
            return HttpResponse(f"Attachment attribute saved.")
        # return redirect('manage-attachments', client.id)


class AttachmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Attachment
    template_name = "attachments/confirm_delete_attachment.html"

    def get_success_url(self):
        return reverse_lazy("manage-attachments", args=(self.get_object().client_id,))

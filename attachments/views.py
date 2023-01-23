from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView

from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from clients.models import Client
from contracts.models import Contract


class AttachmentManageView(LoginRequiredMixin, View):
    form_class = AttachmentUploadForm

    def get(self, request, pk, *args, **kwargs):
        form = AttachmentUploadForm()
        client = Client.objects.get(pk=pk)
        context = {"form": form, "client": client}
        return TemplateResponse(request=request, template="attachments/manage_attachments.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        if len(request.FILES) > 0:
            client = Client.objects.get(pk=pk)
            form = AttachmentUploadForm(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('file')
                for file in files:
                    Attachment.objects.create(
                        client=client,
                        file=file,
                        file_name=file.name,
                    )
        else:
            attachment = Attachment.objects.get(pk=pk)
            client = attachment.client
            attachment.tag = request.POST["attachment_tag"]
            attachment.purpose = request.POST["add_attachment_to"]
            attachment.save()
        return redirect('manage-attachments', client.id)


class AttachmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Attachment
    template_name = "attachments/confirm_delete_attachment.html"

    def get_success_url(self):
        return reverse_lazy("manage-attachments", args=(self.get_object().client_id,))

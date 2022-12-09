from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView

from attachments.forms import AttachmentUploadForm
from attachments.models import Attachment
from clients.models import Client
from contracts.models import Contract


class AttachmentManageView(FormView):
    form_class = AttachmentUploadForm

    def get(self, request, pk, *args, **kwargs):
        form = self.get_form_class()
        client = Client.objects.get(pk=pk)
        context = {"form": form, "client": client}
        return TemplateResponse(request=request, template="attachments/manage_attachments.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        client = Client.objects.get(pk=pk)
        if len(request.FILES) > 0:
            form = AttachmentUploadForm(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('file')
                for file in files:
                    Attachment.objects.create(
                        client=client,
                        file=file,
                    )
        else:
            data = request.POST
            for id, text in data.items():
                if id.isnumeric():
                    attachment = Attachment.objects.get(id=id)
                    attachment.name = text
                    attachment.save()
        return redirect('manage-attachments', client.id)


class AttachmentDeleteView(DeleteView):
    model = Attachment
    template_name = "attachments/confirm_delete_attachment.html"

    def get_success_url(self):
        return reverse_lazy("manage-attachments", args=(self.get_object().contract_id,))

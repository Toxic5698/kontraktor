from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView

from clients.models import Client
from emailing.models import Mail


class ClientMailManageView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        context = {
            "client": Client.objects.get(pk=pk),
            "mails": Mail.objects.filter(client_id=pk).order_by("-created_at")
        }
        return TemplateResponse(template="emailing/client_mail_list.html", context=context, request=request)

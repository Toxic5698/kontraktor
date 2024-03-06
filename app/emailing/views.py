from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView

from clients.models import Client
from emailing.models import Mail
from emailing.services import send_email_service
from operators.models import Operator


class ClientMailManageView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        context = {
            "client": Client.objects.get(pk=pk),
            "mails": Mail.objects.filter(client_id=pk).order_by("-created_at")
        }
        return TemplateResponse(template="emailing/client_mail_list.html", context=context, request=request)


class MailCreateView(LoginRequiredMixin, View):

    def get(self, request, client_id=None, mail_id=None, *args, **kwargs):
        if client_id:
            client = Client.objects.prefetch_related("proposals", "contracts", "protocols").get(pk=client_id)
            mail = Mail.objects.create(
                client=client,
                subject="Nové dokumenty ve službě SAMOSET",
                receiver=client.email,
                created_by=request.user)
            return redirect("edit-mail", mail.id)

        mail = Mail.objects.get(pk=mail_id)
        client = mail.client

        available_documents = []
        available_documents += [{"name": doc.get_name(), "id": doc.id, "type": "n"} for doc in client.proposals.all()]
        available_documents += [{"name": doc.get_name(), "id": doc.id, "type": "c"} for doc in client.contracts.all()]
        available_documents += [{"name": doc.get_name(), "id": doc.id, "type": "p"} for doc in client.protocols.all()]

        chosen_documents = []
        if mail.documents:
            for doc in list(mail.documents.split(",")):
                if "n" in doc:
                    chosen_documents += [doc.get_name() for doc in client.proposals.filter(id=int(doc.strip("n")))]
                if "c" in doc:
                    chosen_documents += [doc.get_name() for doc in client.contracts.filter(id=int(doc.strip("c")))]
                if "p" in doc:
                    chosen_documents += [doc.get_name() for doc in client.protocols.filter(id=int(doc.strip("p")))]

        context = {
            "client": client,
            "mail": mail,
            "available_documents": available_documents,
            "chosen_documents": chosen_documents,
        }
        return TemplateResponse(template="emailing/mail_create.html", context=context, request=request)

    def post(self, request, mail_id, *args, **kwargs):
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        mail = Mail.objects.get(id=mail_id)
        if "add-document" in request.path:
            mail.documents = ",".join(data.keys())
        elif "add-note" in request.path:
            mail.note = data["note"]
        elif "change-receiver" in request.path:
            mail.receiver = data["receiver"]
        elif "change-subject" in request.path:
            mail.subject = data["subject"]
        mail.save()
        return HttpResponse(f"Mail saved.")


class MailPreviewView(LoginRequiredMixin, View):

    def get(self, request, mail_id, *args, **kwargs):
        mail = Mail.objects.get(id=mail_id)
        chosen_documents = []
        if mail.documents:
            for doc in list(mail.documents.split(",")):
                if "n" in doc:
                    chosen_documents += [doc.get_name() for doc in
                                         mail.client.proposals.filter(id=int(doc.strip("n")))]
                if "c" in doc:
                    chosen_documents += [doc.get_name() for doc in
                                         mail.client.contracts.filter(id=int(doc.strip("c")))]
                if "p" in doc:
                    chosen_documents += [doc.get_name() for
                                         doc in mail.client.protocols.filter(id=int(doc.strip("p")))]
        context = {
            "mail": mail,
            "chosen_documents": chosen_documents,
            "link": "http://" + request.META['HTTP_HOST'] + "/clients/" + str(mail.client.sign_code),
            "operator": Operator.objects.get(),
        }
        if "send-mail" in request.path:
            mail = send_email_service(context=context)
            if mail.status == "odeslán":
                messages.success(request, f"E-mail pro {mail.receiver} odeslán.")
            else:
                messages.warning(request, f"E-mail pro {mail.receiver} se nepodařilo odeslat.")
            return redirect("client-mail-list", mail.client.id)
        return TemplateResponse(template="emailing/message_templates/new_document.html",
                                context=context, request=request)


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail

    def get_success_url(self):
        return reverse_lazy("client-mail-list", args=(self.object.client.id,))

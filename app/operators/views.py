from uuid import UUID

from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View

from clients.models import Client
from operators.models import Operator


class WelcomePageView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "operator": Operator.objects.get()
        }
        return TemplateResponse(template="operators/welcome_page.html", request=request, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.get("sign_code")
        if "@" not in data and self.check_uuid(data):
            client = Client.objects.filter(sign_code=data)
            if client.count() == 1:
                return redirect("document-to-sign", data)
            else:
                messages.warning(
                    request, f'Kontaktujte prosím svého prodejce.'
                )
        elif "@" in data:
            client = Client.objects.filter(email=data)
            if client.count() == 1:
                messages.warning(
                    request, f'Odesílám e-mail s kódem na zadanou adresu, zkontrolujte svou e-mailovou schránku.'
                )
            else:
                messages.warning(
                    request, f'Klient s tímto e-mailem nenalezen.'
                )
        else:
            messages.warning(
                request, f'Zadána nesprávná hodnota.'
            )
        return redirect("welcome-page")

    def check_uuid(self, data):
        try:
            UUID(data, version=4)
            return True
        except ValueError:
            return False

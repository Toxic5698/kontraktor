from uuid import UUID

from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View

from clients.models import Client
from emailing.models import Mail
from operators.models import Operator
from operators.services import initial_creation


class WelcomePageView(View):

    def get(self, request, *args, **kwargs):
        operator = Operator.objects.filter()
        if not operator.exists():
            operator = initial_creation()
            messages.info(request,
                          f"Proběhlo prvotní nastavení, zkontrolujte údaje v adminu.")
        elif operator.count() > 1:
            messages.warning(request,
                             f"Sedadlo kontraktoru je přeplněné, zkontrolujte operátora v adminu!")
            return redirect("admin/login")
        context = {
            "operator": operator.get()
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
                    request, f'Kód není správný, překontrolujte jej nebo kontaktujte svého prodejce.'
                )
        elif "@" in data:
            client = Client.objects.filter(email=data)
            if client.count() == 1:
                client = client.get()
                messages.warning(
                    request, f'Odesílám e-mail s kódem na zadanou adresu, zkontrolujte svou e-mailovou schránku.'
                )
                Mail.objects.create(
                    subject=f"Odkaz k dokumentům v Kontraktoru od společnosti {Operator.objects.get()}",
                    message=f"Váš odkaz k dokumentům v Kontraktoru: {request.META['HTTP_HOST']}/clients/{client.sign_code}",
                    recipients=client.email,
                    client=client
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

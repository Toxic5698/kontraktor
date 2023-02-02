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
        return TemplateResponse(template="operators/wp.html", request=request, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.get("sign_code")
        if "@" not in data:
            try:
                client = Client.objects.filter(sign_code=data)
            except ValueError:
                return "špatný"
            if client.count() == 1:
                return redirect("document-to-sign", data)
            else:
                return "špatný"
        elif "@" in data:
            client = Client.objects.filter(email=data)
            if client.count() == 1:
                print("posílám e-mail s odkazem")
            else:
                return "špatný"
        else:
            return "špatný"

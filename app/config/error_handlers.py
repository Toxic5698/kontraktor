from django.shortcuts import render
from django.conf import settings


class CustomExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code in [500, 404] and not settings.DEBUG:
            context = {"path": request.path, "code": response.status_code}
            if response.status_code == 500:
                context["message"] = "Tady jsme to nedomysleli..."
            if response.status_code == 404:
                context["message"] = "Hledali, hledali, ale nenašli..."
            return render(request, 'error.html', context=context)

        return response

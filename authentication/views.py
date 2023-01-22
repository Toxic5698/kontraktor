from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy

from operators.models import Operator


class Login(LoginView):
    template_name = "auth/login.html"
    next_page = reverse_lazy("clients")
    redirect_authenticated_user = reverse_lazy("clients")

    def get_context_data(self, **kwargs):
        context = {
            "operator": Operator.objects.get()
        }
        return context


class Logout(LogoutView):
    next_page = reverse_lazy("login")


class PasswordChange(PasswordChangeView):
    template_name = "auth/password_change.html"

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy

from operators.models import Operator


class Login(LoginView):
    template_name = "auth/../templates/auth/login.html"
    next_page = reverse_lazy("clients")
    redirect_authenticated_user = reverse_lazy("clients")

    def get_context_data(self, **kwargs):
        context = {
            "operator": Operator.objects.get()
        }
        return context


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("login")


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "auth/../templates/auth/password_change.html"

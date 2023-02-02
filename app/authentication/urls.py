from django.urls import path
from authentication.views import *

urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("logout", Logout.as_view(), name="logout"),
    path("password-change", PasswordChange.as_view(), name="password-change"),


]

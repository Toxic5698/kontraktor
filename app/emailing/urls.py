from django.urls import path
from emailing.views import *

urlpatterns = [
    path("<int:pk>/", ClientMailManageView.as_view(), name="client-mail-list"),
]

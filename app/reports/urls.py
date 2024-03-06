from django.urls import path

from reports.views import *

urlpatterns = [
    path("", ReportsView.as_view(), name="reports"),

]

import django_filters
from django.db.models import Q
from django_filters import CharFilter
from clients.models import Client


class ClientFilter(django_filters.FilterSet):
    name_email_address = CharFilter(method="filter_contains")

    class Meta:
        model = Client
        fields = [
            "name_email_address",
        ]

    def filter_contains(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(email__icontains=value) | Q(address__icontains=value))

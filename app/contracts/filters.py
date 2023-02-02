import django_filters
from django.db.models import Q
from django_filters import CharFilter, RangeFilter
from .models import Contract


class ContractFilter(django_filters.FilterSet):
    price = RangeFilter(field_name='price')
    name_email_place_address = CharFilter(method="filter_contains")

    class Meta:
        model = Contract
        fields = ["name_email_place_address", "price"]

    def filter_contains(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(email__icontains=value) |
                               Q(fulfillment_place__icontains=value) | Q(address__icontains=value) |
                               Q(contract_number__icontains=value))


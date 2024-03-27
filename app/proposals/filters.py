import django_filters
from django.db.models import Q
from django_filters import CharFilter, RangeFilter
from proposals.models import Proposal


class ProposalFilter(django_filters.FilterSet):
    price = RangeFilter(field_name='price')
    name_email_place_address = CharFilter(method="filter_contains")

    class Meta:
        model = Proposal
        fields = ["name_email_place_address", "price"]

    def filter_contains(self, queryset, name, value):
        return queryset.filter(Q(client__name__icontains=value) | Q(client__email__icontains=value) |
                               Q(fulfillment_place__icontains=value) | Q(client__address__icontains=value) |
                               Q(document_number__icontains=value))


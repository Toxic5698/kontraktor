from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn

from .models import Contract


class ContractTable(Table):
    edit = LinkColumn('edit-contract', text="Změnit", args=[A("pk")], verbose_name="Změnit", orderable=False)
    delete = LinkColumn('delete-contract', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    show = LinkColumn('parse-contract', text="Zobrazit", args=[A("pk")], verbose_name="Zobrazit", orderable=False)

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ("id", "name", "fulfillment_place", "price", "type", "fulfillment_at", "created_at")
        attrs = {"class": "table table-hover"}

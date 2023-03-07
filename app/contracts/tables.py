from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column, DateColumn, DateTimeColumn

from .models import Contract


class ContractTable(Table):
    delete = LinkColumn('delete-contract', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    contract_number = Column(linkify=("edit-contract", [A("pk")]))
    edited_at = DateTimeColumn(verbose_name="Poslední úprava dne", format="d. m. y h:m")
    client__attachments__filter_contracts__count = Column(verbose_name="Počet příloh", orderable=False)
    proposal__fulfillment_at = DateColumn(verbose_name="Termín plnění", format="d. m. y")
    proposal__items__count = Column(verbose_name="Počet položek", orderable=False)

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ("contract_number", "client__name", "proposal__items__count", "proposal__price",
                  "proposal__fulfillment_at", "proposal__fulfillment_place",
                  "client__attachments__filter_contracts__count", "edited_at", "signed_at",
                  )
        attrs = {"class": "table table-hover table-striped"}

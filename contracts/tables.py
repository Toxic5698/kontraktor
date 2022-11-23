from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column, DateColumn, DateTimeColumn

from .models import Contract


class ContractTable(Table):
    delete = LinkColumn('delete-contract', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    show = LinkColumn('parse-contract', text="Náhled", args=[A("pk")], verbose_name="Zobrazit náhled smlouvy", orderable=False)
    contract_number = Column(verbose_name="Číslo smlouvy", linkify=("edit-contract", [A("pk")]))
    name = Column(verbose_name="Zákazník")
    fulfillment_place = Column(verbose_name="Místo plnění")
    price = Column(verbose_name="Cena")
    fulfillment_at = DateColumn(verbose_name="Čas plnění", format="d. m. y")
    created_at = DateTimeColumn(verbose_name="Vytvořena dne", format="d. m. y h:m")


    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ("contract_number", "name", "price", "fulfillment_place", "fulfillment_at", "created_at")
        attrs = {"class": "table table-hover table-striped"}

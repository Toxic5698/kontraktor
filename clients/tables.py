from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column, DateColumn, DateTimeColumn

from clients.models import Client


class ClientTable(Table):
    delete = LinkColumn('delete-client', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    # edit = LinkColumn('edit-client', text="Upravit", args=[A("pk")], verbose_name="Upravit", orderable=False)
    # proposal = LinkColumn('edit-proposal', text="Nabídka", args=[A("pk")], verbose_name="Nabídka", orderable=False)
    name = Column(linkify=("edit-client", [A("pk")]))

    class Meta:
        model = Client
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("consumer", "name", "id_number", "address", "email", "phone_number")
        attrs = {"class": "table table-hover table-striped"}

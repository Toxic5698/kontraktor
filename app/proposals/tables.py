from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column

from app.proposals.models import Proposal, Item


class ProposalTable(Table):
    delete = LinkColumn('delete-proposal', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    proposal_number = Column(linkify=("edit-proposal", [A("pk")]))

    class Meta:
        model = Proposal
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("proposal_number", "client", "items_quantity", "price", "created_at", "edited_at", )
        attrs = {"class": "table table-hover table-striped"}


class ItemTable(Table):
    delete = LinkColumn('delete-item', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)

    class Meta:
        model = Item
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("priority", "title")

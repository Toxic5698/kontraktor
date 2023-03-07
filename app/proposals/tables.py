from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column

from proposals.models import Proposal, Item


class ProposalTable(Table):
    delete = LinkColumn('delete-proposal', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    proposal_number = Column(linkify=("edit-proposal", [A("pk")]))
    items_quantity = Column(verbose_name="Počet položek", empty_values=(), orderable=False)
    edited = Column(verbose_name="Vytvořená/Upravená", empty_values=(), orderable=False)
    client__attachments__filter_proposals__count = Column(verbose_name="Počet příloh", orderable=False)

    class Meta:
        model = Proposal
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("proposal_number", "client", "items_quantity", "price", "fulfillment_place", "fulfillment_at",
                  "client__attachments__filter_proposals__count", "edited", "signed_at",)
        attrs = {"class": "table table-hover table-striped"}

    def render_items_quantity(self, record, value):
        return record.items.count()

    def render_edited(self, record, value):
        return f"{record.created_at.strftime('%d. %m. %Y')}/{record.edited_at.strftime('%d. %m. %Y')}"


class ItemTable(Table):
    delete = LinkColumn('delete-item', text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)

    class Meta:
        model = Item
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("priority", "title")

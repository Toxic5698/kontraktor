from django.utils.safestring import mark_safe
from django_tables2.utils import A
from django_tables2.tables import Table
from django_tables2 import LinkColumn, Column

from clients.models import Client


class ClientTable(Table):
    delete = LinkColumn("delete-client", text="Smazat", args=[A("pk")], verbose_name="Smazat", orderable=False)
    # edit = LinkColumn('edit-client', text="Upravit", args=[A("pk")], verbose_name="Upravit", orderable=False)
    # proposal = LinkColumn('edit-proposal', text="Nabídka", args=[A("pk")], verbose_name="Nabídka", orderable=False)
    name = Column(linkify=("edit-client", [A("pk")]))
    document_status = Column(verbose_name="Stav dokumentů", empty_values=(), orderable=False)

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "id_number", "address", "email", "phone_number", "document_status")
        attrs = {"class": "table table-hover table-striped"}

    def render_name(self, record, value):
        if record.consumer:
            icon = mark_safe(f'<i class="bi bi-file-person-fill"></i> {value}')
        else:
            icon = mark_safe(f'<i class="bi bi-building-fill"></i> {value}')
        return icon

    def render_document_status(self, record, value):
        proposals, contracts, protocols = "", "", ""
        host = "http://" + self.request.META["HTTP_HOST"]

        if record.proposals.all():
            for proposal in record.proposals.all():
                if proposal.signed_at:
                    proposals += f'<a class="btn btn-success me-1" href="{host}/documents/print/{proposal.client.sign_code}/proposal/{proposal.id}" onclick="runButtonLoader(event)"><i class="bi bi-file-ruled"></i></a>'
                else:
                    proposals += f'<a class="btn btn-primary me-1" href="{host}/proposals/edit/{proposal.id}"><i class="bi bi-file-ruled"></i></a>'
        else:
            proposals = f'<a class="btn btn-secondary me-1"><i class="bi bi-file-ruled"></i></a>'

        if record.contracts.all():
            for contract in record.contracts.all():
                if contract.signed_at:
                    contracts += f'<a class="btn btn-success me-1" href="{host}/documents/print/{contract.client.sign_code}/contract/{contract.id}" onclick="runButtonLoader(event)"><i class="bi bi-file-text"></i></a>'
                else:
                    contracts += f'<a class="btn btn-primary me-1" href="{host}/contracts/edit/{contract.id}"><i class="bi bi-file-text"></i></a>'
        else:
            contracts = f'<a class="btn btn-secondary me-1"><i class="bi bi-file-text"></i></a>'

        if record.protocols.all():
            for protocol in record.protocols.all():
                if protocol.signed_at:
                    protocols += f'<a class="btn btn-success me-1" href="{host}/documents/print/{protocol.client.sign_code}/protocol/{protocol.id}" onclick="runButtonLoader(event)"><i class="bi bi-list-check"></i></a>'
                else:
                    protocols += f'<a class="btn btn-primary me-1" href="{host}/contracts/edit-protocol/{protocol.id}"><i class="bi bi-list-check"></i></a>'
        else:
            protocols = f'<a class="btn btn-secondary me-1"><i class="bi bi-list-check"></i></a>'

        return mark_safe(proposals + contracts + protocols)

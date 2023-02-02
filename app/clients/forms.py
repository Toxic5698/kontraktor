from betterforms.forms import BetterModelForm
from clients.models import Client


class ClientForm(BetterModelForm):
    class Meta:
        model = Client
        fields = "__all__"

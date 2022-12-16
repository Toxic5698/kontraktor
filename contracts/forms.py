from betterforms.forms import BetterModelForm
from .models import Contract


class ContractForm(BetterModelForm):
    class Meta:
        model = Contract
        fields = ("signed_at", "contract_number")

from betterforms.forms import BetterModelForm
from .models import Contract
from django import forms


class ContractForm(BetterModelForm):
    signed_at = forms.DateField(required=False, label="Podepsána dne", widget=forms.TextInput(attrs={'type': "date"}))

    class Meta:
        model = Contract
        fields = ("signed_at", "document_number")

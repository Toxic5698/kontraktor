from django.forms import ModelForm, CharField, ChoiceField, DateTimeField, ModelChoiceField
from betterforms.multiform import MultiForm
from betterforms.forms import BetterModelForm
from .models import Contract


class ContractForm(BetterModelForm):
    class Meta:
        model = Contract
        fields = ("type", "subject", "contract_number",
                  "corporation", "name", "email", "phone_number", "address",
                  "fulfillment_place", "fulfillment_at", "price",
                  "note")

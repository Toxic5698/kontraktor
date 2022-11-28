from betterforms.forms import BetterModelForm
from .models import Contract, Attachment


class ContractForm(BetterModelForm):
    class Meta:
        model = Contract
        fields = ("contract_type", "subject", "contract_number",
                  "consumer", "name", "id_number", "email", "phone_number", "address",
                  "fulfillment_place", "fulfillment_at", "price",
                  "note", "signed_at")


class AttachmentUploadForm(BetterModelForm):
    class Meta:
        model = Attachment
        fields = ("name", "file")

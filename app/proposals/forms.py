from betterforms.forms import BetterModelForm
from django import forms

from proposals.models import Proposal, UploadedProposal


class ProposalUploadForm(BetterModelForm):
    file = forms.FileField(required=False, label="Podkladová nabídka")

    class Meta:
        model = UploadedProposal
        fields = ["file"]


class ProposalEditForm(BetterModelForm):
    fulfillment_at = forms.DateField(
        required=True, label="Termín plnění", widget=forms.TextInput(attrs={"type": "date"})
    )
    signed_at = forms.DateField(required=False, label="Potvrzena dne", widget=forms.TextInput(attrs={"type": "date"}))

    class Meta:
        model = Proposal
        fields = [
            "document_number",
            "signed_at",
            "contract_type",
            "contract_subject",
            "fulfillment_at",
            "fulfillment_place",
        ]

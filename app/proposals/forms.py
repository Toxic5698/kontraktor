from betterforms.forms import BetterModelForm
from django import forms
from app.clients.models import Client
from app.proposals.models import Proposal, UploadedProposal


class ProposalUploadForm(BetterModelForm):
    file = forms.FileField(required=False, label="Podkladová nabídka")

    class Meta:
        model = UploadedProposal
        fields = ['file']


class ProposalEditForm(BetterModelForm):
    fulfillment_at = forms.DateField(required=False, label="Termín plnění",
                                     widget=forms.TextInput(attrs={'type': "date"}))
    signed_at = forms.DateField(required=False, label="Potvrzena dne", widget=forms.TextInput(attrs={'type': "date"}))
    client = forms.ModelChoiceField(label="Klient", queryset=Client.objects.all(), widget=forms.Select(attrs={"readonly": True}))

    class Meta:
        model = Proposal
        fields = ["proposal_number", "signed_at", "contract_type",
                  "contract_type", "subject", "client",
                  "fulfillment_at", "fulfillment_place"]

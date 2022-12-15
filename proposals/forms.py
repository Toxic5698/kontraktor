from betterforms.forms import BetterModelForm, BetterForm
from django import forms

from proposals.models import Proposal, UploadedProposal


class ProposalUploadForm(BetterModelForm):
    file = forms.FileField(required=False, label="Podkladová nabídka")

    class Meta:
        model = UploadedProposal
        fields = ['file']


class ProposalEditForm(BetterModelForm):
    class Meta:
        model = Proposal
        fields = ["proposal_number", "signed_at", "contract_type",
                  "contract_type", "subject", "client",
                  "fulfillment_at", "fulfillment_place"]

from betterforms.forms import BetterModelForm

from proposals.models import Proposal


class ProposalForm(BetterModelForm):
    class Meta:
        model = Proposal

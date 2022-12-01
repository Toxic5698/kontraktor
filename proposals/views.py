from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from proposals.forms import ProposalForm
from proposals.models import Proposal


class ProposalCreateView(CreateView):
    form_class = ProposalForm
    template_name = "proposals/edit_proposal.html"
    success_url = reverse_lazy("proposals")
    model = Proposal


class ProposalUpdateView(UpdateView):
    form_class = ProposalForm
    template_name = "proposals/edit_proposal.html"
    success_url = reverse_lazy("proposals")
    model = Proposal

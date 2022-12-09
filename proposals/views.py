from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, FormView

from proposals.forms import ProposalUploadForm, ProposalEditForm
from proposals.models import Proposal, UploadedProposal
from proposals.peli_parser import parse_items


class ProposalsListView(ListView):
    model = Proposal
    template_name = 'proposals/proposals_list.html'


class ProposalUploadView(FormView):
    form_class = ProposalUploadForm

    def get(self, request, *args, **kwargs):
        form = self.get_form_class()
        context = {
            "form": form,
        }
        return TemplateResponse(template="proposals/upload_proposal.html", request=request, context=context)

    def post(self, request, *args, **kwargs):
        if len(request.FILES) > 0:
            form = ProposalUploadForm(request.POST)
            if form.is_valid():
                file = request.FILES["file"]
                proposal = Proposal.objects.create()
                UploadedProposal.objects.create(
                    file=file,
                    proposal=proposal,
                )
                parse_result = parse_items(file, proposal)
            return redirect('edit-proposal', proposal.id)
        return redirect('upload-proposal')


class ProposalEditView(UpdateView):
    model = Proposal
    template_name = 'proposals/edit_proposal.html'
    form_class = ProposalEditForm

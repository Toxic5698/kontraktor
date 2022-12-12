from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, FormView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from proposals.forms import ProposalUploadForm, ProposalEditForm
from proposals.models import Proposal, UploadedProposal
from proposals.peli_parser import parse_items
from proposals.filters import ProposalFilter
from proposals.tables import ProposalTable


class ProposalsTableView(SingleTableMixin, FilterView):
    table_class = ProposalTable
    model = Proposal
    template_name = "proposals/proposals_list.html"
    filterset_class = ProposalFilter


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


# class ProposalEditView(UpdateView):
#     model = Proposal
#     template_name = 'proposals/edit_proposal.html'
#     form_class = ProposalEditForm
#     success_url = reverse_lazy("proposals")


class ProposalEditView(View):

    def get(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        form = ProposalEditForm(instance=proposal)
        context = {
            "form": form,
        }
        return TemplateResponse(template="proposals/edit_proposal.html", request=request, context=context)

    def post(self, request, pk, *args, **kwargs):
        proposal = Proposal.objects.get(pk=pk)
        form = ProposalEditForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()

        return redirect('edit-proposal', proposal.id)



class ProposalCreateView(CreateView):
    model = Proposal
    template_name = 'proposals/edit_proposal.html'
    form_class = ProposalEditForm


class ProposalDeleteView(DeleteView):
    model = Proposal
    template_name = 'proposals/confirm_delete_proposal.html'
    success_url = reverse_lazy("proposals")

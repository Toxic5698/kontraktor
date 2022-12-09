from django.contrib.admin import site
from django.contrib import admin

from proposals.models import Proposal, UploadedProposal, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class UploadedProposalInline(admin.TabularInline):
    model = UploadedProposal
    extra = 0


class ProposalAdmin(admin.ModelAdmin):
    model = Proposal
    fields = ("proposal_number", "price", )
    inlines = [UploadedProposalInline, ItemInline]


class UploadedProposalAdmin(admin.ModelAdmin):
    model = UploadedProposal
    fields = ("file", "file_name", "priority", "proposal")


site.register(Proposal, ProposalAdmin)
site.register(UploadedProposal, UploadedProposalAdmin)

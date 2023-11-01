from django.contrib.admin import site
from django.contrib import admin

from proposals.models import Proposal, UploadedProposal, Item, ContractType, ContractSubject, DefaultItem


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class UploadedProposalInline(admin.TabularInline):
    model = UploadedProposal
    extra = 0


class ProposalAdmin(admin.ModelAdmin):
    model = Proposal
    fields = ("proposal_number", "price_netto", )
    inlines = [UploadedProposalInline, ItemInline]


class DefaultItemAdmin(admin.ModelAdmin):
    model = DefaultItem
    fields = ("subject", "contract_type", "title", "description", "production_price", "price_per_unit", "unit")

class UploadedProposalAdmin(admin.ModelAdmin):
    model = UploadedProposal
    fields = ("file", "file_name", "priority", "proposal")


class ContractTypeAdmin(admin.ModelAdmin):
    model = ContractType
    fields = ("type", "name")


class ContractSubjectAdmin(admin.ModelAdmin):
    model = ContractSubject
    fields = ("code", "name")


site.register(Proposal, ProposalAdmin)
site.register(UploadedProposal, UploadedProposalAdmin)
site.register(ContractType, ContractTypeAdmin)
site.register(ContractSubject, ContractSubjectAdmin)
site.register(DefaultItem, DefaultItemAdmin)

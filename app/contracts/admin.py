from django.contrib import admin
from django.contrib.admin import site

from contracts.models import Contract, ContractCore, ContractSection


class ContractCoreInline(admin.TabularInline):
    model = ContractCore.contract.through


class ContractAdmin(admin.ModelAdmin):
    model = Contract
    fields = ["contract_number", "signed_at"]
    list_display = ["contract_number", "client"]
    inlines = [ContractCoreInline,]


class ContractCoreAdmin(admin.ModelAdmin):
    model = ContractCore
    fields = ["contract_type", "parent_id", "contract_section", "priority", "text", "essential", "editable", "default",
              "created_at", "created_by", "edited_at", "edited_by", "note"
              ]
    readonly_fields = ["created_at", ]
    list_display = ["contract_section", "priority", "essential", "editable", "default",
                    "created_at", "created_by", "edited_at", "edited_by",]
    list_filter = ["contract_section", "essential", "editable", "default", "created_at", "created_by", "edited_at", "edited_by",]


class ContractSectionAdmin(admin.ModelAdmin):
    model = ContractSection
    fields = ["priority", "name", "contract_type"]
    list_display = ["priority", "name", "contract_type"]
    list_filter = ["priority", "name", "contract_type"]


site.register(Contract, ContractAdmin)
site.register(ContractCore, ContractCoreAdmin)
site.register(ContractSection, ContractSectionAdmin)

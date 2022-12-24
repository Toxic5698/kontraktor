from django.contrib import admin
from django.contrib.admin import site

from contracts.models import Contract, ContractCore


class ContractAdmin(admin.ModelAdmin):
    model = Contract
    fields = ["contract_number", "signed_at"]


class ContractCoreAdmin(admin.ModelAdmin):
    model = ContractCore
    fields = ["contract_type", "parent_id", "section", "priority", "text", "essential", "editable", "default",
              "created_at", "created_by", "edited_at", "edited_by", "note"
              ]
    readonly_fields = ["created_at", ]
    list_display = ["section", "priority", "text", "essential", "editable", "default",
                    "created_at", "created_by", "edited_at", "edited_by",]
    list_filter = ["section", "essential", "editable", "default", "created_at", "created_by", "edited_at", "edited_by",]


site.register(Contract, ContractAdmin)
site.register(ContractCore, ContractCoreAdmin)

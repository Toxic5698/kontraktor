from django.contrib import admin
from django.contrib.admin import site

from contracts.models import Contract, ContractCore, Attachment


class ContractCoreAdmin(admin.ModelAdmin):
    model = ContractCore
    fields = ["contract_type", "parent_id", "section", "priority", "text", "essential", "editable", "default",
              "created_at", "created_by", "edited_at", "edited_by", "note"
              ]
    readonly_fields = ["created_at", ]
    list_display = ["section", "priority", "text", "essential", "editable", "default",
                    "created_at", "created_by", "edited_at", "edited_by",]
    list_filter = ["section", "essential", "editable", "default", "created_at", "created_by", "edited_at", "edited_by",]


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ("name", "file", "added_by", "contract")
    list_display = ["name", "file", "added_by", "contract", ]


site.register(ContractCore, ContractCoreAdmin)
site.register(Attachment, AttachmentAdmin)

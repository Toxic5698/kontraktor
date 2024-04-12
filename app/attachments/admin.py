from django.contrib.admin import site
from django.contrib import admin

from attachments.models import Attachment, DefaultAttachment


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ("file_name", "file", "tag", "created_by", "client")
    list_display = ["file_name", "file", "tag", "created_by", "client"]


class DefaultAttachmentAdmin(admin.ModelAdmin):
    model = DefaultAttachment
    fields = ("file_name", "file", "tag", "contract_subject", "contract_type", "document_type")
    list_display = ["file_name", "file", "tag"]


site.register(Attachment, AttachmentAdmin)
site.register(DefaultAttachment, DefaultAttachmentAdmin)

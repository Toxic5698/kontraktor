from django.contrib.admin import site
from django.contrib import admin

from attachments.models import Attachment, DefaultAttachment


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ("file_name", "file", "tag", "added_by", "client", "purpose")
    list_display = ["file_name", "file", "tag", "added_by", "client", "purpose"]


class DefaultAttachmentAdmin(admin.ModelAdmin):
    model = DefaultAttachment
    fields = ("file_name", "file", "tag", "subject", "contract_type", "purpose")
    list_display = ["file_name", "file", "tag", "subject", "contract_type", "purpose"]



site.register(Attachment, AttachmentAdmin)
site.register(DefaultAttachment, DefaultAttachmentAdmin)

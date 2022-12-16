from django.contrib.admin import site
from django.contrib import admin

from attachments.models import Attachment


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    fields = ("file_name", "file", "tag", "added_by", "client")
    list_display = ["file_name", "file", "tag", "added_by", "client", ]


site.register(Attachment, AttachmentAdmin)

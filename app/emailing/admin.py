from django.contrib.admin import site, ModelAdmin

from emailing.models import Mail


class MailAdmin(ModelAdmin):
    model = Mail
    fields = ["client", "subject", "status"]
    list_display = ["subject", "created_at", "status", "client"]
    list_filter = ["subject", "status"]
    search_fields = ["subject", "client"]


site.register(Mail, MailAdmin)

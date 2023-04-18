from django.contrib.admin import site, ModelAdmin

from emailing.models import Mail


class MailAdmin(ModelAdmin):
    model = Mail
    fields = ["client", "recipients", "subject", "message", "sent"]
    list_display = ["recipients", "subject", "created_at", "sent", "client"]
    list_filter = ["subject", "message", "sent"]
    search_fields = ["recipients", "subject", "message", "client"]


site.register(Mail, MailAdmin)

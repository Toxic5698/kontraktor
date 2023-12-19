from django.contrib.admin import site, ModelAdmin

from emailing.models import Mail


class MailAdmin(ModelAdmin):
    model = Mail
    fields = ["client", "subject", "sent"]
    list_display = ["subject", "created_at", "sent", "client"]
    list_filter = ["subject", "sent"]
    search_fields = ["subject", "client"]


site.register(Mail, MailAdmin)

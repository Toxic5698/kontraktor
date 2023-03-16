from django.contrib.admin import ModelAdmin, site

from operators.models import Operator


class OperatorAdmin(ModelAdmin):
    fields = ["name", "address", "id_number", "bank_number", "acting_person", "web", "email", "phone_number"]
    list_display = ["name", "address", "id_number", "bank_number", "acting_person", "web"]
    model = Operator


site.register(Operator, OperatorAdmin)

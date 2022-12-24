from django.contrib.admin import ModelAdmin, site

from operators.models import Operator


class OperatorAdmin(ModelAdmin):
    fields = ["name", "address", "id_number", "bank_number", "acting_person"]
    list_display = ["name", "address", "id_number", "bank_number", "acting_person"]
    model = Operator


site.register(Operator, OperatorAdmin)

from django.contrib import admin

from clients.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "id_number", "email", "address", "phone_number", "note", "consumer")

    class Meta:
        fields = ("name", "id_number", "email", "address", "phone_number", "note", "consumer")


admin.site.register(Client, ClientAdmin)

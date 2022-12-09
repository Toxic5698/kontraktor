from django.db.models import Model, CharField, DateField, TextField, BooleanField


class Client(Model):
    name = CharField(max_length=255, blank=True, null=True, verbose_name="Jméno")
    id_number = CharField(max_length=12, blank=True, null=True, verbose_name="Datum narození nebo IČ")
    address = CharField(max_length=1000, blank=True, null=True, verbose_name="Adresa bydliště nebo sídla")
    email = CharField(max_length=255, blank=True, null=True, verbose_name="E-mailová adresa")
    phone_number = CharField(max_length=12, blank=True, null=True, verbose_name="Telefonní číslo")
    note = TextField(max_length=1000, blank=True, null=True, verbose_name="Poznámka")
    consumer = BooleanField(default=True, verbose_name="Spotřebitel (fyzická osoba)")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name

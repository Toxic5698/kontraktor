import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, CharField, DateField, TextField, BooleanField, UUIDField, ForeignKey, CASCADE, \
    DateTimeField, FileField, PositiveIntegerField, Index, ImageField


class Client(Model):
    name = CharField(max_length=255, blank=True, null=True, verbose_name="Jméno")
    id_number = CharField(max_length=12, blank=True, null=True, verbose_name="Datum narození nebo IČ")
    address = CharField(max_length=1000, blank=True, null=True, verbose_name="Adresa bydliště nebo sídla")
    email = CharField(max_length=255, blank=True, null=True, verbose_name="E-mailová adresa")
    phone_number = CharField(max_length=12, blank=True, null=True, verbose_name="Telefonní číslo")
    note = TextField(max_length=1000, blank=True, null=True, verbose_name="Poznámka")
    consumer = BooleanField(default=True, verbose_name="Spotřebitel (fyzická osoba)")
    sign_code = UUIDField(default=uuid.uuid4, verbose_name="Kód pro potvrzení", editable=False, unique=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name

def signature_directory_path(instance, file):
    return f"{instance.client_id}/signatures/{file}"


class Signature(Model):
    client = ForeignKey(Client, on_delete=CASCADE, related_name="signatures", verbose_name="Klient")
    created_at = DateTimeField(auto_now_add=True, verbose_name="Vytvořen")
    file = ImageField(upload_to=signature_directory_path, blank=True, null=True, verbose_name="Obrázek podpisu")
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField(null=True, blank=True)
    document_object = GenericForeignKey('content_type', 'object_id')
    ip = CharField(null=True, blank=True, max_length=300, verbose_name="IP adresa clienta")

    class Meta:
        verbose_name = "Signature"
        verbose_name_plural = "Signatures"
        indexes = [Index(fields=['content_type', 'object_id']), ]

    def __str__(self):
        return f"{self.client} signature"

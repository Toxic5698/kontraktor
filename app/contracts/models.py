from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CharField, TextField, SET_NULL, \
    CASCADE, OneToOneField, IntegerField

from attachments.models import Attachment
from base.models import UserBaseModel, DateBaseModel
from clients.models import Client, Signature
from documents.models import Document, DocumentParagraph
from proposals.models import Proposal, Item


class Contract(Document):
    proposal = OneToOneField(Proposal, verbose_name="Nabídka", on_delete=CASCADE, null=True, related_name="sister")

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return f"{self.document_number}"


class Protocol(Document):
    contract = ForeignKey(Contract, on_delete=CASCADE, related_name="protocols", verbose_name="Smlouva")
    priority = IntegerField(verbose_name="Číslo protokolu", default=1)

    class Meta:
        verbose_name = "Handover Protocol"
        verbose_name_plural = "Handover Protocols"

    def __str__(self):
        return f"{self.contract}"

    def save(self, *args, **kwargs):
        last_protocol_priority = Protocol.objects.filter(contract=self.contract).count()
        self.priority = last_protocol_priority + 1
        super().save(*args, **kwargs)


class ProtocolItem(UserBaseModel, DateBaseModel):
    STATUS = [
        ("yes", "Předáno"),
        ("with_note", "Předáno s výhradou"),
        ("no", "Nepředáno"),
    ]
    protocol = ForeignKey(Protocol, on_delete=CASCADE, related_name="items", verbose_name="Předávací protokol")
    item = ForeignKey(Item, on_delete=SET_NULL, related_name="items", verbose_name="Položka", null=True)
    description = TextField(null=True, blank=True, verbose_name="Upřesnění")
    status = CharField(max_length=20, blank=False, null=False, verbose_name="Stav", choices=STATUS)

    class Meta:
        verbose_name = "Handover protocol item"
        verbose_name_plural = "Handover protocol items"

from django.contrib.auth.models import User
from django.db.models import Model, CharField, BooleanField, DateTimeField, SET_NULL, ForeignKey, TextField, ManyToManyField

from clients.models import Client
from contracts.models import Contract, Protocol
from emailing.enums import EmailStatusOptions
from proposals.models import Proposal


class Mail(Model):
    client = ForeignKey(Client, on_delete=SET_NULL, blank=True, null=True, related_name="mails", verbose_name="Klient")
    subject = CharField(max_length=1000, blank=False, null=False, verbose_name="Předmět zprávy")
    sender = CharField(max_length=50, blank=True, null=True, verbose_name="Odesílatel")
    receiver = CharField(max_length=50, blank=True, null=True, verbose_name="Adresát")
    message = TextField(verbose_name="Obsah zprávy") # HTMLfield?
    created_at = DateTimeField(auto_now_add=True, verbose_name="Vytvořen dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="mail_created_by",
                            verbose_name="Vytvořil")
    status = CharField(default="vytvořen", verbose_name="Stav", max_length=30, choices=EmailStatusOptions.choices)
    documents = TextField(blank=True, null=True, verbose_name="Týká se dokumentů")
    note = TextField(blank=True, null=True, verbose_name="Poznámka")

    class Meta:
        verbose_name = "E-mail"
        verbose_name_plural = "E-maily"

    def __str__(self):
        return f"{self.receiver} - {self.subject}"

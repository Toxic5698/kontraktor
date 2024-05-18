from django.db.models import CharField, CASCADE, ForeignKey, TextField

from base.models import BaseModel, UserBaseModel
from clients.models import Client
from emailing.enums import EmailStatusOptions


class Mail(UserBaseModel, BaseModel):
    client = ForeignKey(Client, on_delete=CASCADE, blank=False, null=False, related_name="mails", verbose_name="Klient")
    subject = CharField(max_length=1000, blank=False, null=False, verbose_name="Předmět zprávy")
    sender = CharField(max_length=50, blank=True, null=True, verbose_name="Odesílatel")  # TODO: ForeignKey na User?
    receiver = CharField(max_length=50, blank=True, null=True, verbose_name="Adresát")
    message = TextField(verbose_name="Obsah zprávy")  # HTMLfield?
    status = CharField(default="vytvořen", verbose_name="Stav", max_length=30, choices=EmailStatusOptions.choices)
    documents = TextField(blank=True, null=True, verbose_name="Týká se dokumentů")  # TODO: ManyToManyField na dokumenty?

    class Meta:
        verbose_name = "E-mail"
        verbose_name_plural = "E-maily"

    def __str__(self):
        return f"{self.receiver} - {self.subject}"

from django.db.models import Model, CharField, BooleanField, DateTimeField, SET_NULL, ForeignKey, TextField

from clients.models import Client


class Mail(Model):
    client = ForeignKey(Client, on_delete=SET_NULL, blank=True, null=True, related_name="mails", verbose_name="Klient")
    subject = CharField(max_length=1000, blank=False, null=False, verbose_name="Předmět zprávy")
    sender = CharField(max_length=50, blank=True, null=True, verbose_name="Odesílatel")
    message = TextField(verbose_name="Obsah zprávy") # HTMLfield?
    created_at = DateTimeField(auto_now_add=True, verbose_name="Vytvořen")
    sent = BooleanField(default=False, verbose_name="Odeslán")

    class Meta:
        verbose_name = "E-mail"
        verbose_name_plural = "E-maily"

    def __str__(self):
        return f"{self.client.email} - {self.subject}"

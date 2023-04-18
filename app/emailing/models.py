import sentry_sdk
from email_validator import validate_email, EmailNotValidError
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Model, CharField, BooleanField, DateTimeField, SET_NULL, ForeignKey

from clients.models import Client


class Mail(Model):
    client = ForeignKey(Client, on_delete=SET_NULL, blank=True, null=True, related_name="mails", verbose_name="Klient")
    subject = CharField(max_length=1000, blank=False, null=False, verbose_name="Předmět zprávy")
    message = CharField(max_length=1000, blank=False, null=False, verbose_name="Obsah zprávy")
    recipients = CharField(max_length=1000, blank=False, null=False, verbose_name="Adresát")
    created_at = DateTimeField(auto_now_add=True, verbose_name="Vytvořen")
    sent = BooleanField(default=False, verbose_name="Odeslán")

    class Meta:
        verbose_name = "E-mail"
        verbose_name_plural = "E-maily"

    def __str__(self):
        return f"{self.subject} - {self.recipients}"

    def save(self, *args, **kwargs):
        if not self.sent:
            send_mail(subject=self.subject, message=self.message, recipient_list=self.get_recipient_list(),
                      from_email=settings.EMAIL_HOST_USER)
            self.sent = True
        else:
            sentry_sdk.capture_message(f"Pokus odeslat znovu e-mail {self.id} - {self.recipients}")
        super().save(*args, **kwargs)

    def get_recipient_list(self):
        recipient_list = []
        for recipient in self.recipients.split(","):
            try:
                email = validate_email(recipient, check_deliverability=True)
                recipient_list.append(email.normalized)
            except EmailNotValidError:
                sentry_sdk.capture_message(f"{recipient} is not valid e-mail or not deliverable.")
        return recipient_list

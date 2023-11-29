from django.contrib.auth.models import User
from django.db.models import Model, CharField, FileField, DateTimeField, ForeignKey, SET_NULL, CASCADE, ManyToManyField

from clients.models import Client
from attachments.managers import AttachmentManager
from proposals.models import ContractSubject, ContractType


def attachment_directory_path(instance, file):
    return f"{instance.client.sign_code}/attachments/{file}"


def default_attachment_directory_path(instance, file):
    return f"default_attachments/{file}"


class BaseAttachment(Model):
    PURPOSES = [
        ("intern", "intern"),
        ("proposal", "proposal"),
        ("contract", "contract"),
        ("both", "both"),
        ("protocol", "protocol"),
    ]
    tag = CharField(max_length=255, blank=True, verbose_name="Označení souboru")
    file_name = CharField(max_length=255, blank=True, null=True, verbose_name="Název souboru")
    purpose = CharField(max_length=10, null=True, blank=True, choices=PURPOSES, default="intern",
                        verbose_name="Účel přílohy")

    class Meta:
        abstract = True


class Attachment(BaseAttachment):
    added_at = DateTimeField(auto_now_add=True, verbose_name="přidána dne")
    added_by = ForeignKey(User, related_name="attachments", on_delete=SET_NULL, blank=True, null=True,
                          verbose_name="přidána uživatelem")
    client = ForeignKey(Client, blank=True, null=True, on_delete=SET_NULL, related_name="attachments",
                        verbose_name="klient")
    file = FileField(upload_to=attachment_directory_path, blank=True, null=True, verbose_name="Soubor")

    objects = AttachmentManager()

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return self.tag or self.file_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class DefaultAttachment(BaseAttachment):
    subject = ForeignKey(ContractSubject, related_name="default_attachment", on_delete=CASCADE,
                         verbose_name="předmět smlouvy")
    contract_type = ForeignKey(ContractType, related_name="default_attachment", on_delete=CASCADE, verbose_name="typ smlouvy")
    client = ManyToManyField(Client, related_name="default_attachments", blank=True)
    file = FileField(upload_to=default_attachment_directory_path, blank=True, null=True, verbose_name="Soubor")

    objects = AttachmentManager()

    class Meta:
        verbose_name = "Default Attachment"
        verbose_name_plural = "Default Attachments"

    def __str__(self):
        return f"{self.file_name} - {self.subject} - {self.contract_type}"

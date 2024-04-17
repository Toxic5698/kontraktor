from django.db.models import CharField, FileField, ForeignKey, SET_NULL, ManyToManyField

from attachments.managers import AttachmentManager
from base.models import UserBaseModel, DateBaseModel, ContractTypeAndSubjectMixin
from clients.models import Client
from documents.enums import DocumentTypeOptions


def attachment_directory_path(instance, file):
    return f"{instance.client.sign_code}/attachments/{file}"


def default_attachment_directory_path(instance, file):
    return f"default_attachments/{file}"


class BaseAttachment(UserBaseModel, DateBaseModel):
    tag = CharField(max_length=255, blank=True, verbose_name="Označení souboru")
    file_name = CharField(max_length=255, blank=True, null=True, verbose_name="Název souboru")

    class Meta:
        abstract = True


class Attachment(BaseAttachment):
    client = ForeignKey(
        Client, blank=True, null=True, on_delete=SET_NULL, related_name="attachments", verbose_name="Klient"
    )
    file = FileField(upload_to=attachment_directory_path, blank=True, null=True, verbose_name="Soubor")

    objects = AttachmentManager()

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return self.tag or self.file_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def is_intern(self):
        if self.proposals.all().exists() or self.contracts.all().exists() or self.protocols.all().exists():
            return False
        return True

    def change_to_intern(self, data):
        if data == "intern" and not self.is_intern():
            self.proposals.clear()
            self.contracts.clear()
            self.protocols.clear()


class DefaultAttachment(BaseAttachment, ContractTypeAndSubjectMixin):
    client = ManyToManyField(Client, related_name="default_attachments", blank=True, verbose_name="Klient")
    file = FileField(upload_to=default_attachment_directory_path, blank=True, null=True, verbose_name="Soubor")
    document_type = CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Typ dokumentu",
        choices=DocumentTypeOptions.choices,
        default="contract",
    )

    objects = AttachmentManager()

    class Meta:
        verbose_name = "Default Attachment"
        verbose_name_plural = "Default Attachments"

    def __str__(self):
        return f"{self.file_name} - {self.contract_subject} - {self.contract_type}"

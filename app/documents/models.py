from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    CharField,
    ForeignKey,
    SET_NULL,
    DateField,
    IntegerField,
    ManyToManyField,
    CASCADE,
    TextField,
    BooleanField,
    Q,
)

from attachments.models import Attachment, DefaultAttachment
from base.models import UserBaseModel, BaseModel, ContractTypeAndSubjectMixin
from clients.models import Signature, Client
from documents.enums import DocumentTypeOptions
from documents.managers import DocumentParagraphManager


class DocumentSection(UserBaseModel, BaseModel, ContractTypeAndSubjectMixin):
    priority = IntegerField(verbose_name="Číslo oddílu")
    name = CharField(max_length=200, null=False, blank=True, verbose_name="Název oddílu")

    class Meta:
        verbose_name = "Document section"
        verbose_name_plural = "Document sections"

    def __str__(self):
        return f"{self.name} - {self.contract_type}"


class DocumentParagraph(UserBaseModel, BaseModel, ContractTypeAndSubjectMixin):
    document_type = CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Typ dokumentu",
        choices=DocumentTypeOptions.choices,
        default="contract",
    )
    document_section = ForeignKey(
        DocumentSection, on_delete=SET_NULL, verbose_name="Oddíl", related_name="document_paragraphs", null=True
    )
    priority = IntegerField(verbose_name="Číslo ustanovení", blank=False, null=False)
    text = TextField(max_length=10000, blank=True, null=True, verbose_name="Text ustanovení")
    essential = BooleanField(default=False, verbose_name="Nepominutelné")
    editable = BooleanField(default=True, verbose_name="Upravitelné")
    default = BooleanField(default=True, verbose_name="Původní")
    parent_id = CharField(blank=True, null=True, verbose_name="ID původního ustanovení")

    objects = DocumentParagraphManager()

    class Meta:
        verbose_name = "Document Paragraph"
        verbose_name_plural = "Document Paragraphs"
        unique_together = ["priority", "text", "document_section"]
        ordering = [
            "priority",
        ]

    def __str__(self):
        return f"{self.document_type}.{self.priority} - {self.default}"


class Document(UserBaseModel, BaseModel, ContractTypeAndSubjectMixin):
    client = ForeignKey(Client, related_name="%(class)ss", on_delete=CASCADE, verbose_name="klient", null=False)
    document_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo dokumentu")
    signed_at = DateField(blank=True, null=True, verbose_name="Potvrzen dne")
    signatures = GenericRelation(Signature, verbose_name="Podpisy", related_query_name="protocol")
    paragraphs = ManyToManyField(DocumentParagraph, related_name="%(class)ss", verbose_name="Ustanovení")
    attachments = ManyToManyField(Attachment, related_name="%(class)ss", verbose_name="Přílohy")
    default_attachments = ManyToManyField(
        DefaultAttachment, related_name="%(class)ss", verbose_name="Automatické přílohy"
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        document_type = self.__class__.__name__.lower()
        if self.paragraphs.count() == 0:
            paragraphs = DocumentParagraph.objects.filter(
                Q(
                    Q(contract_subject__isnull=True) | Q(contract_subject=self.contract_subject),
                    Q(contract_type__isnull=True) | Q(contract_type=self.contract_type),
                ),
                document_type=document_type,
                default=True,
            )
            self.paragraphs.set(paragraphs)
        if self.default_attachments.count() == 0:
            default_attachments = DefaultAttachment.objects.filter(
                Q(
                    Q(contract_subject__isnull=True) | Q(contract_subject=self.contract_subject),
                    Q(contract_type__isnull=True) | Q(contract_type=self.contract_type),
                ),
                document_type=document_type,
            )
            if default_attachments.exists():
                self.default_attachments.set(default_attachments)

    def get_name(self):
        model_dict = {"Proposal": "Nabídka", "Contract": "Smlouva", "Protocol": "Předávací protokol"}
        model = model_dict.get(self.__class__.__name__)
        if model == "protocol":
            return f"{model} č {self.priority} ke smlouvě č. {self.contract.document_number}"
        return f"{model} č. {self.document_number}"

    def get_class_id(self):
        return f"{self.__class__.__name__}.{self.id}"

    def get_document_type(self):
        return f"{self.__class__.__name__.lower()}"

    def get_document_attachments(self):
        attachments = []
        for attachment in self.attachments.all():
            attachments.append(attachment)
        for default_attachment in self.default_attachments.all():
            attachments.append(default_attachment)
        return attachments

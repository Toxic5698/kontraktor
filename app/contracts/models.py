from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField, DateField, CASCADE, OneToOneField
from django.utils import timezone

from clients.models import Client, Signature
from proposals.models import Proposal, ContractType, Item, ContractSubject
from attachments.models import Attachment


class Contract(Model):
    contract_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo smlouvy")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_created_by",
                            verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_edited_by",
                           verbose_name="Upravil")
    signed_at = DateField(blank=True, null=True, verbose_name="Podepsána dne")
    proposal = OneToOneField(Proposal, verbose_name="Nabídka", on_delete=CASCADE, null=True)
    client = ForeignKey(Client, on_delete=CASCADE, related_name="contracts", null=True)
    signatures = GenericRelation(Signature, verbose_name="Podpisy", related_query_name="contract")

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return f"{self.contract_number}"

    def save(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)
        if self.contract_cores.count() == 0:
            cores = ContractCore.objects.filter(default=True, contract_type=self.proposal.contract_type)
            self.contract_cores.set(cores)

    def get_name(self):
        return f"Smlouva č. {self.contract_number}"


class ContractSection(Model):
    priority = IntegerField(verbose_name="Číslo oddílu")
    name = CharField(max_length=200, null=False, blank=True, verbose_name="Název oddílu")
    contract_type = ForeignKey(ContractType, on_delete=CASCADE, related_name="contract_sections",
                               verbose_name="Typ smlouvy")

    class Meta:
        verbose_name = "Contract section"
        verbose_name_plural = "Contract sections"

    def __str__(self):
        return f"{self.name} - {self.contract_type}"


class ContractCore(Model):
    priority = IntegerField(verbose_name="Číslo ustanovení")
    subject = ForeignKey(ContractSubject, related_name="contract_cores", on_delete=SET_NULL,
                         verbose_name="Předmět smlouvy", null=True)
    contract_type = ForeignKey(ContractType, on_delete=SET_NULL, verbose_name="Typ smlouvy", null=True)
    contract_section = ForeignKey(ContractSection, on_delete=SET_NULL, verbose_name="Oddíl",
                                  related_name="contract_cores", null=True)
    text = TextField(max_length=10000, blank=True, null=True, verbose_name="Text ustanovení")
    essential = BooleanField(default=False, verbose_name="Nepominutelné")
    editable = BooleanField(default=True, verbose_name="Upravitelné")
    default = BooleanField(default=True, verbose_name="Původní")
    contract = ManyToManyField(Contract, related_name="contract_cores", verbose_name="Smlouva")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False)
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_created_by")
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_edited_by")
    parent_id = IntegerField(blank=True, null=True, verbose_name="ID původního ustanovení")
    note = TextField(max_length=1000, blank=True, null=True, verbose_name="Poznámka")

    class Meta:
        verbose_name = "Contract Core"
        verbose_name_plural = "Contract Cores"
        unique_together = ["priority", "text", "contract_section"]
        ordering = ["priority", ]

    def __str__(self):
        return f"{self.contract_section.name}.{self.priority} - {self.default}"

    def save(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)


class Protocol(Model):
    contract = ForeignKey(Contract, on_delete=CASCADE, related_name="protocols", verbose_name="Smlouva")
    client = ForeignKey(Client, on_delete=CASCADE, related_name="protocols", verbose_name="Klient", null=True)
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořen dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="protocol_created_by",
                            verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upraven dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="protocol_edited_by",
                           verbose_name="Upravil")
    signed_at = DateField(blank=True, null=True, verbose_name="Podepsán dne")
    signatures = GenericRelation(Signature, verbose_name="Podpisy", related_query_name="protocol")
    note = TextField(blank=True, null=True, verbose_name="Poznámka k protokolu")

    class Meta:
        verbose_name = "Handover Protocol"
        verbose_name_plural = "Handover Protocols"

    def __str__(self):
        return f"{self.contract}"

    def get_name(self):
        date = self.signed_at if self.signed_at else self.edited_at
        return f"Předávací protokol ke smlouvě č. {self.contract.contract_number} ze dne {date if date else self.created_at}"


class ProtocolItem(Model):
    STATUS = [
        ("yes", "Předáno"),
        ("with_note", "Předáno s výhradou"),
        ("no", "Nepředáno"),
    ]
    protocol = ForeignKey(Protocol, on_delete=CASCADE, related_name="items", verbose_name="Předávací protokol")
    item = ForeignKey(Item, on_delete=SET_NULL, related_name="items", verbose_name="Položka", null=True)
    description = TextField(null=True, blank=True, verbose_name="Upřesnění")
    note = TextField(blank=True, null=True, verbose_name="Poznámka")
    status = CharField(max_length=20, blank=False, null=False, verbose_name="Stav", choices=STATUS)
    created_at = DateField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořen dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="protocol_item_created_by",
                            verbose_name="Vytvořil")

    class Meta:
        verbose_name = "Handover protocol item"
        verbose_name_plural = "Handover protocol items"

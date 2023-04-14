from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField, DateField, CASCADE, OneToOneField
from django.utils import timezone

from clients.models import Client, Signature
from proposals.models import Proposal, ContractType
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
            return print(self.contract_cores.count())


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
    contract_type = ManyToManyField(ContractType, related_name="contract_cores")
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
        unique_together = ["priority", "text"]
        ordering = ["priority", ]

    def __str__(self):
        return f"{self.contract_section.name}.{self.priority} - {self.default}"

    def save(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)

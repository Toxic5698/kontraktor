from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField, DateField, CASCADE, OneToOneField
from django.utils import timezone

from clients.models import Client
from proposals.models import Proposal, ContractType
from contracts.constants import *


class Contract(Model):
    contract_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo smlouvy")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_created_by", verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_edited_by", verbose_name="Upravil")
    signed_at = DateField(blank=True, null=True, verbose_name="Podepsána dne")
    proposal = OneToOneField(Proposal, verbose_name="Nabídka", on_delete=CASCADE, null=True)
    client = ForeignKey(Client, on_delete=CASCADE, related_name="contracts", null=True)

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


class ContractCore(Model):
    section = CharField(max_length=100, blank=True, null=True, verbose_name="Oddíl", choices=CONTRACT_SECTIONS)
    priority = IntegerField()
    contract_type = ManyToManyField(ContractType, related_name="contract_cores")
    text = TextField(max_length=10000, blank=True, null=True)
    essential = BooleanField(default=False)
    editable = BooleanField(default=True)
    default = BooleanField(default=True)

    contract = ManyToManyField(Contract, related_name="contract_cores")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False)
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_created_by")
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_edited_by")
    parent_id = IntegerField(blank=True, null=True)
    note = TextField(max_length=1000, blank=True, null=True,)

    class Meta:
        verbose_name = "Contract Core"
        verbose_name_plural = "Contract Cores"
        unique_together = ["priority", "text"]
        ordering = ["priority", ]

    def __str__(self):
        return f"{self.priority} - {self.default}"

    def save(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)


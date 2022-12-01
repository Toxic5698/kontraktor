from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField, DateField, FileField

from contracts.constants import CONTRACT_SUBJECTS
from contracts.models import ContractType


class Proposal(Model):
    proposal_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo nabídky")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_created_by", verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_edited_by", verbose_name="Upravil")
    signed_at = DateTimeField(blank=True, null=True, verbose_name="Podepsána dne")

    contract_type = ForeignKey(ContractType, related_name="proposals", on_delete=SET_NULL, verbose_name="Typ smlouvy", null=True)
    subject = CharField(blank=True, null=True, max_length=100, choices=CONTRACT_SUBJECTS, verbose_name="Předmět nabídky")
    price = CharField(max_length=20, verbose_name="Cena")
    fulfillment_at = DateField(null=True, blank=True, verbose_name="Čas plnění")
    fulfillment_place = CharField(max_length=1000, verbose_name="Místo plnění")

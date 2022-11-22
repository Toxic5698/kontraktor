from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField
from .constants import *


class Contract(Model):
    contract_number = CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False)
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_created_by")
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_edited_by")
    signed_at = DateTimeField(blank=True, null=True)

    type = CharField(blank=True, null=True, max_length=8, choices=CONTRACT_TYPES)
    subject = CharField(blank=True, null=True, max_length=100, choices=CONTRACT_SUBJECTS)
    price = CharField(max_length=20)
    fulfillment_at = DateTimeField(null=True, blank=True)
    fulfillment_place = CharField(max_length=1000)

    name = CharField(max_length=255, blank=True, null=True,)
    id_number = CharField(max_length=8, blank=True, null=True,)
    address = CharField(max_length=1000, blank=True, null=True,)
    email = CharField(max_length=255, blank=True, null=True,)
    phone_number = CharField(max_length=12, blank=True, null=True,)
    note = TextField(max_length=1000, blank=True, null=True,)
    corporation = BooleanField(default=False)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return print("not created")
        cores = ContractCore.objects.filter(essential=True, default=True) # přidat type_usage negativní nebo pozitivní filtr?
        instance.contract_cores = cores
        return print("created")


class ContractCore(Model):
    priority = IntegerField()
    type_usage = CharField(max_length=8, blank=True, null=True, choices=CONTRACT_TYPES)
    text = TextField(max_length=10000, blank=True, null=True)
    essential = BooleanField(default=False)
    editable = BooleanField(default=True)
    default = BooleanField(default=True)

    contract = ManyToManyField(Contract, related_name="contract_cores")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False)
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_created_by")
    edited_at = DateTimeField(blank=True, null=True)
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_core_edited_by")
    parent_id = CharField(blank=True, null=True, max_length=4)
    note = TextField(max_length=1000, blank=True, null=True,)


class Attachment(Model):
    name = CharField(max_length=255, blank=True)
    file = CharField(max_length=255, blank=True)
    added_at = DateTimeField(auto_now_add=True)
    added_by = ForeignKey(User, related_name="attachments", on_delete=SET_NULL, blank=True, null=True)
    contract = ForeignKey(Contract, blank=True, null=True, on_delete=SET_NULL, related_name="attachments")


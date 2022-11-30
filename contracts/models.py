from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, TextField, BooleanField, SET_NULL, \
    IntegerField, ManyToManyField, DateField, FileField
from .constants import *


class ContractType(Model):
    type = CharField(max_length=255, blank=False, null=False)
    name = CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return self.name


class Contract(Model):
    contract_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo smlouvy")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_created_by", verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="contract_edited_by", verbose_name="Upravil")
    signed_at = DateTimeField(blank=True, null=True, verbose_name="Podepsána dne")

    contract_type = ForeignKey(ContractType, related_name="contracts", on_delete=SET_NULL, verbose_name="Typ smlouvy", null=True)
    subject = CharField(blank=True, null=True, max_length=100, choices=CONTRACT_SUBJECTS, verbose_name="Předmět smlouvy")
    price = CharField(max_length=20, verbose_name="Cena")
    fulfillment_at = DateField(null=True, blank=True, verbose_name="Čas plnění")
    fulfillment_place = CharField(max_length=1000, verbose_name="Místo plnění")

    name = CharField(max_length=255, blank=True, null=True, verbose_name="Jméno")
    id_number = CharField(max_length=12, blank=True, null=True, verbose_name="Datum narození nebo IČ")
    address = CharField(max_length=1000, blank=True, null=True, verbose_name="Adresa bydliště nebo sídla")
    email = CharField(max_length=255, blank=True, null=True, verbose_name="E-mailová adresa")
    phone_number = CharField(max_length=12, blank=True, null=True, verbose_name="Telefonní číslo")
    note = TextField(max_length=1000, blank=True, null=True, verbose_name="Poznámka")
    consumer = BooleanField(default=True, verbose_name="Spotřebitel (fyzická osoba)")

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return f"{self.contract_number} - {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.contract_cores.count() == 0:
            cores = ContractCore.objects.filter(default=True, contract_type=self.contract_type)
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


class Attachment(Model):
    name = CharField(max_length=255, blank=True)
    file = FileField(upload_to="attachments/", blank=True, null=True) # rozlišit podle smluv
    added_at = DateTimeField(auto_now_add=True)
    added_by = ForeignKey(User, related_name="attachments", on_delete=SET_NULL, blank=True, null=True)
    contract = ForeignKey(Contract, blank=True, null=True, on_delete=SET_NULL, related_name="attachments")

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return self.name or str(self.file)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

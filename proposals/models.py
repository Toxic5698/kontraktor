from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, SET_NULL, \
    IntegerField, DateField, FileField, DecimalField, CASCADE

from clients.models import Client
from contracts.constants import CONTRACT_SUBJECTS
from contracts.models import ContractType


class Proposal(Model):
    proposal_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo nabídky")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_created_by", verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_edited_by", verbose_name="Upravil")
    signed_at = DateTimeField(blank=True, null=True, verbose_name="Potvrzena dne")

    contract_type = ForeignKey(ContractType, related_name="proposals", on_delete=SET_NULL, verbose_name="Typ smlouvy", null=True)
    subject = CharField(blank=True, null=True, max_length=100, choices=CONTRACT_SUBJECTS, verbose_name="Předmět nabídky")
    price = CharField(max_length=20, verbose_name="Cena")
    fulfillment_at = DateField(null=True, blank=True, verbose_name="Čas plnění")
    fulfillment_place = CharField(max_length=1000, verbose_name="Místo plnění")
    client = ForeignKey(Client, related_name="proposals", on_delete=SET_NULL, verbose_name="klient", null=True, blank=True)

    class Meta:
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"

    # def __str__(self):
    #     return self.proposal_number


def uploaded_proposal_directory_path(instance, file):
    return f"attachments/{instance.client_id}/{file}"


class UploadedProposal(Model):
    priority = CharField(max_length=3, null=True, blank=True, verbose_name="pořadí")
    file = FileField(upload_to=uploaded_proposal_directory_path, null=True, blank=True, verbose_name="soubor")
    file_name = CharField(max_length=200, null=True, blank=True, verbose_name="název souboru")
    proposal = ForeignKey(Proposal, on_delete=CASCADE, blank=True, verbose_name="nabídka", related_name="uploaded")

    class Meta:
        verbose_name = "UploadedProposal"
        verbose_name_plural = "UploadedProposals"
        ordering = ['priority']

    # def __str__(self):
    #     return self.file

    def save(self, *args, **kwargs):
        from proposals.peli_parser import parse_items
        # self.priority = 1
        # self.file_name = "soubor 1"
        super().save(*args, **kwargs)
        if self.proposal.items.count() == 0:
            parse_items(self.file, self.proposal)


class Item(Model):
    priority = IntegerField(null=True, verbose_name="pořadí", blank=True)
    title = CharField(max_length=200, blank=True, null=True, verbose_name="název")
    description = CharField(max_length=1000, blank=True, null=True, verbose_name="popis")
    price = DecimalField(decimal_places=2, max_digits=10, verbose_name="cena", null=True, blank=True)
    discount = IntegerField(null=True, blank=True, verbose_name="sleva")
    quantity = IntegerField(null=True, blank=True, verbose_name="množství")
    production_date = CharField(max_length=50, blank=True, null=True, verbose_name="výrobní termín")
    proposal = ForeignKey(Proposal, on_delete=CASCADE, blank=True, null=True, verbose_name="nabídka",
                          related_name="items")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['priority', ]

    def __str__(self):
        return f"{self.priority} - {self.title}"


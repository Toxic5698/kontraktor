from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, SET_NULL, \
    IntegerField, DateField, FileField, DecimalField, CASCADE, BooleanField, Sum, TextChoices

from clients.models import Client
from contracts.constants import CONTRACT_SUBJECTS
from contracts.models import ContractType
from decimal import Decimal


class Proposal(Model):
    proposal_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo nabídky")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_created_by",
                            verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_edited_by",
                           verbose_name="Upravil")
    signed_at = DateTimeField(blank=True, null=True, verbose_name="Potvrzena dne")

    contract_type = ForeignKey(ContractType, related_name="proposals", on_delete=SET_NULL, verbose_name="Typ smlouvy",
                               null=True)
    subject = CharField(blank=True, null=True, max_length=100, choices=CONTRACT_SUBJECTS,
                        verbose_name="Předmět nabídky")
    price = DecimalField(max_digits=20, decimal_places=2, verbose_name="Cena", blank=True, null=True)
    fulfillment_at = DateField(null=True, blank=True, verbose_name="Čas plnění")
    fulfillment_place = CharField(max_length=1000, verbose_name="Místo plnění", null=True, blank=True)
    client = ForeignKey(Client, related_name="proposals", on_delete=SET_NULL, verbose_name="klient", null=True,
                        blank=True)

    class Meta:
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"

    def __str__(self):
        return self.proposal_number

    def save(self, *args, **kwargs):
        if self.items.all():
            self.price = self.items.all().aggregate(Sum("sale_price"))["sale_price__sum"]
            check_payments(self)
        super(Proposal, self).save(*args, **kwargs)


def uploaded_proposal_directory_path(instance, file):
    return f"{instance.proposal.client_id}/uploaded/{file}"


class UploadedProposal(Model):
    priority = CharField(max_length=3, null=True, blank=True, verbose_name="pořadí")
    file = FileField(upload_to=uploaded_proposal_directory_path, null=True, blank=True,
                     verbose_name="Podkladová nabídka")
    file_name = CharField(max_length=200, null=True, blank=True, verbose_name="název souboru")
    proposal = ForeignKey(Proposal, on_delete=CASCADE, blank=True, verbose_name="nabídka", related_name="uploaded")
    uploaded_at = DateTimeField(auto_now_add=True, blank=True, verbose_name="Nahráno dne", null=True)

    class Meta:
        verbose_name = "UploadedProposal"
        verbose_name_plural = "UploadedProposals"
        ordering = ['uploaded_at']

    def __str__(self):
        return self.file_name

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
    production_price = DecimalField(decimal_places=2, max_digits=10, verbose_name="cena", null=True, blank=True)
    sale_price = DecimalField(decimal_places=2, max_digits=10, verbose_name="cena", null=True, blank=True)
    sale_discount = IntegerField(null=True, blank=True, verbose_name="sleva")
    revenue = DecimalField(null=True, blank=True, verbose_name="zisk", decimal_places=2, max_digits=10)
    quantity = IntegerField(null=True, blank=True, verbose_name="množství")
    production_date = CharField(max_length=50, blank=True, null=True, verbose_name="výrobní termín")
    production_data = CharField(max_length=1000, blank=True, null=True, verbose_name="výrobní data")
    from_upload = BooleanField(default=False, verbose_name="nahraná položka")

    proposal = ForeignKey(Proposal, on_delete=CASCADE, blank=True, null=True, verbose_name="nabídka",
                          related_name="items")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['priority', ]

    def __str__(self):
        return f"{self.priority} - {self.title}"

    def clean(self, **kwargs):
        self.priority = self.get_priority() if not self.priority else self.priority
        self.title = kwargs.get('title') or self.title if self.title else ""
        self.description = kwargs.get('description') or self.description if self.description else ""
        self.production_price = self.price_format(data=kwargs.get('production_price')) or \
                                Decimal(self.production_price) if self.production_price else 0
        self.sale_price = self.price_format(data=kwargs.get('sale_price')) or \
                          Decimal(self.sale_price) if self.sale_price else 0
        self.sale_discount = self.number_format(data=kwargs.get('sale_discount')) or self.sale_discount if self.sale_discount else 0
        self.quantity = self.number_format(data=kwargs.get('quantity')) or self.quantity if self.quantity else 0
        self.production_date = kwargs.get('production_date') or self.production_date if self.production_date else ""
        self.production_data = kwargs.get('production_data') or self.production_data if self.production_data else ""

    def save(self, *args, **kwargs):
        self.clean(**kwargs)
        if self.production_price and self.sale_price:
            self.revenue = self.sale_price - self.production_price
        super(Item, self).save()
        self.proposal.save()

    def get_priority(self):
        last = self.proposal.items.all().order_by('priority').last().priority
        return last + 1

    def price_format(self, data=None):
        if data is None:
            return None
        if "," in data:
            data = data.replace(",", ".").replace("\xa0", "")
            price = Decimal(data)
            return price
        return ValueError("Price in wrong format.")

    def number_format(self, data=None):
        if data is None:
            return None
        return int(data)


class Payment(Model):
    class DueOptions(TextChoices):
        AFTER_SIGN = "10", "po podpisu smlouvy"
        BEFORE_DELIVERY = "21", "před dodáním"
        AFTER_DELIVERY = "31", "po dodání"
        AFTER_COMPLETION = "32", "po dokončení"
        BEFORE_COMPLETION = "22", "před dokončením"
        EMPTY = "99", "-"

    amount = DecimalField(max_digits=10, decimal_places=2, verbose_name="výše")
    part = IntegerField(verbose_name="část z celku")
    due = CharField(max_length=100, default=DueOptions.EMPTY, choices=DueOptions.choices, verbose_name="splatnost")
    proposal = ForeignKey(Proposal, on_delete=CASCADE, related_name="payments", verbose_name="nabídka")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["due", ]

    def __str__(self):
        return f"{self.get_due_display()} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.part == 0 or self.part == "":
            self.due = "99"
            self.part = 0
        if int(self.part) > 0 and self.due == "99":
            raise ValueError(f"U platby {self} musí být nastavená splatnost.")

        super(Payment, self).save(*args, **kwargs)


def check_payments(proposal):
    if not proposal.payments.all():
        Payment.objects.create(
            proposal=proposal,
            amount=proposal.price,
            part=100,
            due="10"
        )
        Payment.objects.create(
            proposal=proposal, part=0, amount=Decimal(0))
        Payment.objects.create(
            proposal=proposal, part=0, amount=Decimal(0))
    else:
        if proposal.payments.all().aggregate(Sum("part"))["part__sum"] != 100:
            raise ValueError("Souhrn částí plateb se nerovná celku.")
        else:
            for payment in proposal.payments.all():
                payment.amount = proposal.price * (payment.part / Decimal(100))
                payment.save()
    return True

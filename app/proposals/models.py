from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, CharField, SET_NULL, \
    IntegerField, DateField, FileField, DecimalField, CASCADE, BooleanField, Sum, TextField
from django.utils import timezone

from clients.models import Client
from decimal import Decimal

from proposals.enums import UnitOptions, DueOptions
from proposals.managers import PaymentManager


class ContractType(Model):
    type = CharField(max_length=255, blank=False, null=False)
    name = CharField(max_length=255, blank=False, null=True)
    vat = IntegerField(default=21)

    def __str__(self):
        return self.name


class ContractSubject(Model):
    code = CharField(max_length=255, blank=False, null=False)
    name = CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return self.name


class Proposal(Model):
    proposal_number = CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Číslo nabídky")
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořena dne")
    created_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_created_by",
                            verbose_name="Vytvořil")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upravena dne")
    edited_by = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL, related_name="proposal_edited_by",
                           verbose_name="Upravil")
    signed_at = DateField(blank=True, null=True, verbose_name="Potvrzena dne")
    contract_type = ForeignKey(ContractType, related_name="proposals", on_delete=SET_NULL, verbose_name="Typ smlouvy",
                               null=True)
    subject = ForeignKey(ContractSubject, related_name="proposals", on_delete=SET_NULL, verbose_name="Předmět nabídky",
                         null=True)
    price_netto = DecimalField(max_digits=20, decimal_places=2, verbose_name="Cena bez DPH", blank=True, null=True)
    price_brutto = DecimalField(max_digits=20, decimal_places=2, verbose_name="Cena s DPH", blank=True, null=True)
    fulfillment_at = DateField(null=True, blank=True, verbose_name="Termín plnění")
    fulfillment_place = CharField(max_length=1000, verbose_name="Místo plnění", null=True, blank=True)
    client = ForeignKey(Client, related_name="proposals", on_delete=CASCADE, verbose_name="klient", null=True,
                        blank=True)

    class Meta:
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"

    def __str__(self):
        if self.proposal_number:
            return self.proposal_number
        else:
            return f"Objednávka ID {self.id} bez čísla"

    def save(self, *args, **kwargs):
        if self.id:
            if self.items.all():
                self.price_netto = self.items.all().aggregate(Sum("total_price"))["total_price__sum"]
                self.price_brutto = self.price_netto * Decimal((100 + self.contract_type.vat) / 100)
                check_payments(self)
        self.edited_at = timezone.now()
        super(Proposal, self).save(*args, **kwargs)


def uploaded_proposal_directory_path(instance, file):
    return f"{instance.proposal.client.sign_code}/uploaded/{file}"


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


class AbstractItem(Model):
    title = CharField(max_length=200, blank=True, null=True, verbose_name="název")
    description = CharField(max_length=1000, blank=True, null=True, verbose_name="popis")
    production_price = DecimalField(decimal_places=2, max_digits=10, verbose_name="nákladová cena za jednotku",
                                    null=True, blank=True)
    price_per_unit = DecimalField(decimal_places=2, max_digits=10, verbose_name="cena ze jednotku", null=True,
                                  blank=True)
    unit = CharField(max_length=5, verbose_name="jednotka", null=True, blank=True,
                     choices=UnitOptions.choices, default="ks")

    class Meta:
        abstract = True
        verbose_name = "Abstract Item"
        verbose_name_plural = "Abstract Items"


class Item(AbstractItem):
    priority = IntegerField(null=True, verbose_name="pořadí", blank=True)
    total_price = DecimalField(decimal_places=2, max_digits=10, verbose_name="celková cena", null=True, blank=True)
    sale_discount = IntegerField(null=True, blank=True, verbose_name="sleva", default=0)
    revenue = DecimalField(null=True, blank=True, verbose_name="zisk", decimal_places=2, max_digits=10)
    quantity = IntegerField(null=True, blank=True, verbose_name="množství")
    production_date = CharField(max_length=50, blank=True, null=True, verbose_name="výrobní termín")
    production_data = TextField(blank=True, null=True, verbose_name="výrobní data")
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
        if "price_per_unit" in kwargs.keys(): # data from edit form
            for key in kwargs.keys():
                if key in ["production_price", "price_per_unit"]:
                    setattr(self, key, self.price_format(kwargs[key]))
                elif key in ["sale_discount", "quantity"]:
                    setattr(self, key, self.number_format(kwargs[key]))
                else:
                    setattr(self, key, kwargs[key])
        else: # data from create form and upload
            self.production_price = Decimal(self.production_price) if self.production_price else 0
            self.price_per_unit = Decimal(self.price_per_unit) if self.price_per_unit else 0
            self.sale_discount = int(self.sale_discount) if self.sale_discount else 0
            self.quantity = int(self.quantity) if self.quantity else 1

    def save(self, *args, **kwargs):
        self.clean(**kwargs)
        if self.production_price and self.price_per_unit:
            self.revenue = self.get_revenue()
        if self.price_per_unit and self.quantity:
            self.total_price = (int(self.price_per_unit) * int(self.quantity)) * (
                    (100 - int(self.sale_discount)) / 100)
        else:
            self.total_price = self.price_per_unit
        super(Item, self).save()
        self.proposal.save()

    def get_priority(self):
        if self.proposal.items.all():
            last = self.proposal.items.all().order_by('priority').last().priority
            return last + 1
        return 1

    def price_format(self, data=None):
        if data is None or type(data) == Decimal:
            return data
        if data == "":
            data = 0
        if "," in data:
            data = data.replace(",", ".").replace("\xa0", "")
        try:
            price = Decimal(data)
            return price
        except ValueError:
            return ValueError("Price in wrong format.")

    def number_format(self, data=None):
        if data is None or data == "":
            return 0
        return int(data)

    def get_revenue(self):
        production_price = int(self.production_price)
        price_per_unit = int(self.price_per_unit)
        quantity = int(self.quantity)
        discount = int(self.sale_discount)
        revenue = ((price_per_unit * quantity) * ((100 - discount) / 100)) - (
                production_price * quantity)
        return Decimal(revenue)


class DefaultItem(AbstractItem):
    subject = ForeignKey(ContractSubject, related_name="default_item", on_delete=CASCADE,
                         verbose_name="předmět smlouvy")
    contract_type = ForeignKey(ContractType, related_name="default_item", on_delete=CASCADE, verbose_name="typ smlouvy")

    class Meta:
        verbose_name = "Default Item"
        verbose_name_plural = "Default Items"

    def __str__(self):
        return f"{self.contract_type} - {self.subject} - {self.title}"


class Payment(Model):
    amount = DecimalField(max_digits=10, decimal_places=2, verbose_name="výše")
    part = IntegerField(verbose_name="část z celku")
    due = CharField(max_length=100, default=DueOptions.EMPTY, choices=DueOptions.choices, verbose_name="splatnost")
    proposal = ForeignKey(Proposal, on_delete=CASCADE, related_name="payments", verbose_name="nabídka")

    objects = PaymentManager()

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
            return False

        super(Payment, self).save(*args, **kwargs)
        return True


def check_payments(proposal):
    if not proposal.payments.all():
        Payment.objects.create(
            proposal=proposal,
            amount=proposal.price_brutto,
            part=100,
            due="10"
        )
        Payment.objects.create(
            proposal=proposal, part=0, amount=Decimal(0))
        Payment.objects.create(
            proposal=proposal, part=0, amount=Decimal(0))
    else:
        if proposal.payments.all().aggregate(Sum("part"))["part__sum"] != 100:
            return False
        else:
            for payment in proposal.payments.all():
                payment.amount = proposal.price_brutto * (payment.part / Decimal(100))
                payment.save()
    return True

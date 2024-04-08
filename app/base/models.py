from django.contrib.auth.models import User
from django.db.models import Model, DateTimeField, ForeignKey, SET_NULL, TextField, CharField, IntegerField
from django.utils import timezone


class UserBaseModel(Model):
    created_by = ForeignKey(
        User, blank=True, null=True, on_delete=SET_NULL, related_name="%(class)s_created_by", verbose_name="Vytvořil"
    )
    edited_by = ForeignKey(
        User, blank=True, null=True, on_delete=SET_NULL, related_name="%(class)s_edited_by", verbose_name="Upravil"
    )

    class Meta:
        abstract = True


class DateBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name="Vytvořeno dne")
    edited_at = DateTimeField(blank=True, null=True, verbose_name="Upraveno dne")
    note = TextField(blank=True, null=True, verbose_name="Poznámka")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)


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


class ContractTypeAndSubjectMixin(Model):
    contract_type = ForeignKey(
        ContractType, related_name="%(class)ss", on_delete=SET_NULL, verbose_name="Typ smlouvy", null=True, blank=True
    )
    contract_subject = ForeignKey(
        ContractSubject,
        related_name="%(class)ss",
        on_delete=SET_NULL,
        verbose_name="Předmět smlouvy",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

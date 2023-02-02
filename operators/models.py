from django.db.models import Model, CharField


class Operator(Model):
    name = CharField(max_length=100, verbose_name="Název společnosti")
    address = CharField(max_length=256, verbose_name="Sídlo")
    id_number = CharField(max_length=9, verbose_name="IČ")
    bank_number = CharField(max_length=30, verbose_name="Číslo účtu")
    acting_person = CharField(max_length=200, verbose_name="Zastoupená...")
    web = CharField(max_length=100, verbose_name="Link operátora", null=True, blank=True)

    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"

    def __str__(self):
        return self.name


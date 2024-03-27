from django.db.models import Model, CharField, IntegerField


class Operator(Model):
    name = CharField(max_length=100, verbose_name="Název společnosti")
    address = CharField(max_length=256, verbose_name="Sídlo")
    id_number = CharField(max_length=9, verbose_name="IČ")
    bank_number = CharField(max_length=30, verbose_name="Číslo účtu")
    acting_person = CharField(max_length=200, verbose_name="Zastoupená...")
    web = CharField(max_length=100, verbose_name="Link operátora", null=True, blank=True)
    email = CharField(max_length=100, verbose_name="Email", null=True, blank=True)
    phone_number = CharField(max_length=100, verbose_name="Telefon", null=True, blank=True)
    proposal_validity = IntegerField(default=14)
    # logo_file_name
    # signature_file_name
    # pdf_style_file_name
    # pdf_font


    class Meta:
        verbose_name = "Operator"
        verbose_name_plural = "Operators"

    def __str__(self):
        return self.name



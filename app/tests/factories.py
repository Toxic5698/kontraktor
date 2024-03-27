import factory
from django.contrib.auth.models import AnonymousUser
from factory import SubFactory, LazyAttribute, django

from faker import Faker

from base.models import *
from clients.models import *
from proposals.models import *
from operators.models import Operator

faker = Faker(["cs_CZ"])


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    username = LazyAttribute(lambda _: faker.unique.email())
    password = LazyAttribute(lambda _: faker.password())
    is_staff = True
    is_superuser = True

class OperatorFactory(django.DjangoModelFactory):
    class Meta:
        model = Operator

    name = LazyAttribute(lambda _: faker.company())
    address = LazyAttribute(lambda _: faker.address())
    id_number = LazyAttribute(lambda _: faker.passport_number())
    bank_number = LazyAttribute(lambda _: faker.iban())
    acting_person = LazyAttribute(lambda _: faker.name())
    web = LazyAttribute(lambda _: faker.url())
    email = LazyAttribute(lambda _: faker.email())
    phone_number = LazyAttribute(lambda _: faker.phone_number())
    id = LazyAttribute(lambda _: faker.random_digit_not_null())


class ContractTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = ContractType

    type = "DILO"
    name = "Smlouva o dílo"
    vat = 15


class ContractSubjectFactory(django.DjangoModelFactory):
    class Meta:
        model = ContractSubject

    code = "DVERE"
    name = "dveře"


class ClientFactory(django.DjangoModelFactory):
    class Meta:
        model = Client

    name = LazyAttribute(lambda _: faker.name())
    id_number = LazyAttribute(lambda _: faker.passport_number())
    address = LazyAttribute(lambda _: faker.address())
    email = LazyAttribute(lambda _: faker.email())
    phone_number = LazyAttribute(lambda _: faker.phone_number())
    # operator = Operator.objects.get()


class ProposalFactory(django.DjangoModelFactory):
    class Meta:
        model = Proposal

    client = factory.SubFactory(ClientFactory)
    document_number = LazyAttribute(lambda _: faker.bothify(text="??####"))
    contract_type = factory.Iterator(ContractType.objects.all())
    contract_subject = factory.Iterator(ContractSubject.objects.all())
    price_netto = LazyAttribute(lambda _: faker.random_digit_not_null())
    fulfillment_at = LazyAttribute(lambda _: faker.date())
    fulfillment_place = LazyAttribute(lambda _: faker.city())


class ItemFactory(django.DjangoModelFactory):
    class Meta:
        model = Item

    title = LazyAttribute(lambda _: faker.text(max_nb_chars=20))
    description = LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    production_date = LazyAttribute(lambda _: faker.date())
    production_price = LazyAttribute(lambda _: faker.random_int(min=1000, max=1500))
    price_per_unit = LazyAttribute(lambda _: faker.random_int(min=2000, max=2500))
    unit = factory.Iterator(UnitOptions)
    quantity = LazyAttribute(lambda _: faker.random_digit_not_null())
    sale_discount = LazyAttribute(lambda _: faker.random_digit_not_null())

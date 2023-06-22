from factory import SubFactory, LazyAttribute, django

from faker import Faker

from clients.models import *
from proposals.models import *
from operators.models import Operator

faker = Faker()


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
    id_number = "555566666"
    address = LazyAttribute(lambda _: faker.address())
    email = LazyAttribute(lambda _: faker.email())
    phone_number = "555566666"

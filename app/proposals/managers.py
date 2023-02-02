from django.db.models import Manager, Q


class PaymentManager(Manager):
    def filter_contracts(self):
        return super().get_queryset().filter(proposal=self.instance, amount__gt=0)

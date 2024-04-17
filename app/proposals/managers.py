from django.db.models import Manager


class PaymentManager(Manager):
    def filter_not_null(self):
        return super().get_queryset().filter(proposal=self.instance, amount__gt=0)

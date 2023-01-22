from django.db.models import Manager, Q


class AttachmentManager(Manager):
    def filter_contracts(self):
        return super().get_queryset().filter(Q(client=self.instance), Q(purpose="contract") | Q(purpose="both"))

    def filter_proposals(self):
        return super().get_queryset().filter(Q(client=self.instance), Q(purpose="proposal") | Q(purpose="both"))

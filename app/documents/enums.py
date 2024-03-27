from django.db.models import TextChoices


class DocumentTypeOptions(TextChoices):
    PROPOSAL = "proposal"
    CONTRACT = "contract"
    PROTOCOL = "protocol"

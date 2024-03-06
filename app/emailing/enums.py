from django.db.models import TextChoices


class EmailStatusOptions(TextChoices):
    SENT = "odeslán"
    CREATED = "vytvořen"
    FAILED = "nepodařilo se odeslat"

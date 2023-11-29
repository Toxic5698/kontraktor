from django.db.models import TextChoices


class UnitOptions(TextChoices):
    KS = "ks"
    KG = "kg"
    LITERS = "l"
    CUBIC_METERS = "mb"
    SQUARE_METERS = "m2"
    HOURS = "hod"


class DueOptions(TextChoices):
    AFTER_SIGN = "10", "po podpisu smlouvy"
    BEFORE_DELIVERY = "21", "před dodáním"
    AFTER_DELIVERY = "31", "po dodání"
    AFTER_COMPLETION = "32", "po dokončení"
    BEFORE_COMPLETION = "22", "před dokončením"
    EMPTY = "99", "-"

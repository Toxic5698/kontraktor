from django.contrib.auth.models import User
from django.db.models import Model, CharField, FileField, DateTimeField, ForeignKey, SET_NULL, BooleanField

from clients.models import Client


def attachment_directory_path(instance, file):
    return f"attachments/{instance.client_id}/{file}"


class Attachment(Model):
    name = CharField(max_length=255, blank=True)
    file = FileField(upload_to=attachment_directory_path, blank=True, null=True) # rozlišit podle smluv
    added_at = DateTimeField(auto_now_add=True)
    added_by = ForeignKey(User, related_name="attachments", on_delete=SET_NULL, blank=True, null=True)
    client = ForeignKey(Client, blank=True, null=True, on_delete=SET_NULL, related_name="attachments")
    add_to_proposal = BooleanField(default=False)
    add_to_contract = BooleanField(default=False)

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return self.name or str(self.file)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


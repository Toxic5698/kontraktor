from django.contrib.auth.models import User
from django.db.models import Model, CharField, FileField, DateTimeField, ForeignKey, SET_NULL

from clients.models import Client
from attachments.managers import AttachmentManager


def attachment_directory_path(instance, file):
    return f"{instance.client_id}/attachments/{file}"


class Attachment(Model):
    PURPOSES = [
        ("intern", "intern"),
        ("proposal", "proposal"),
        ("contract", "contract"),
        ("both", "both"),
    ]
    tag = CharField(max_length=255, blank=True)
    file_name = CharField(max_length=255, blank=True, null=True)
    file = FileField(upload_to=attachment_directory_path, blank=True, null=True)
    added_at = DateTimeField(auto_now_add=True)
    added_by = ForeignKey(User, related_name="attachments", on_delete=SET_NULL, blank=True, null=True)
    client = ForeignKey(Client, blank=True, null=True, on_delete=SET_NULL, related_name="attachments")
    purpose = CharField(max_length=10, null=True, blank=True, choices=PURPOSES)

    objects = AttachmentManager()

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

    def __str__(self):
        return self.tag or self.file_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


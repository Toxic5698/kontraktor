# Generated by Django 4.2.11 on 2024-05-18 11:41

import charidfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ulid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mail",
            fields=[
                ("is_removed", models.BooleanField(default=False)),
                (
                    "id",
                    charidfield.fields.CharIDField(
                        default=ulid.ULID,
                        editable=False,
                        max_length=26,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Id",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Vytvořeno dne")),
                ("edited_at", models.DateTimeField(blank=True, editable=False, null=True, verbose_name="Upraveno dne")),
                ("note", models.TextField(blank=True, null=True, verbose_name="Poznámka")),
                ("subject", models.CharField(max_length=1000, verbose_name="Předmět zprávy")),
                ("sender", models.CharField(blank=True, max_length=50, null=True, verbose_name="Odesílatel")),
                ("receiver", models.CharField(blank=True, max_length=50, null=True, verbose_name="Adresát")),
                ("message", models.TextField(verbose_name="Obsah zprávy")),
                (
                    "status",
                    models.CharField(
                        choices=[("odeslán", "Sent"), ("vytvořen", "Created"), ("nepodařilo se odeslat", "Failed")],
                        default="vytvořen",
                        max_length=30,
                        verbose_name="Stav",
                    ),
                ),
                ("documents", models.TextField(blank=True, null=True, verbose_name="Týká se dokumentů")),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mails",
                        to="clients.client",
                        verbose_name="Klient",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Vytvořil",
                    ),
                ),
                (
                    "edited_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_edited_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Upravil",
                    ),
                ),
            ],
            options={
                "verbose_name": "E-mail",
                "verbose_name_plural": "E-maily",
            },
        ),
    ]

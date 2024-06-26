# Generated by Django 4.2.11 on 2024-03-25 15:31

import clients.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno dne')),
                ('edited_at', models.DateTimeField(blank=True, null=True, verbose_name='Upraveno dne')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Poznámka')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Jméno')),
                ('id_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Datum narození nebo IČ')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Adresa bydliště nebo sídla')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mailová adresa')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefonní číslo')),
                ('consumer', models.BooleanField(default=True, verbose_name='Spotřebitel (fyzická osoba)')),
                ('sign_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Kód pro potvrzení')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Vytvořil')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_edited_by', to=settings.AUTH_USER_MODEL, verbose_name='Upravil')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno dne')),
                ('edited_at', models.DateTimeField(blank=True, null=True, verbose_name='Upraveno dne')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Poznámka')),
                ('file', models.ImageField(blank=True, null=True, upload_to=clients.models.signature_directory_path, verbose_name='Obrázek podpisu')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=300, null=True, verbose_name='IP adresa clienta')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to='clients.client', verbose_name='Klient')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'Signatures',
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='clients_sig_content_16121b_idx')],
            },
        ),
    ]

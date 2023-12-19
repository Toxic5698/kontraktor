# Generated by Django 4.1.3 on 2023-11-08 13:13

import clients.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Jméno')),
                ('id_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Datum narození nebo IČ')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Adresa bydliště nebo sídla')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mailová adresa')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefonní číslo')),
                ('note', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Poznámka')),
                ('consumer', models.BooleanField(default=True, verbose_name='Spotřebitel (fyzická osoba)')),
                ('sign_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Kód pro potvrzení')),
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
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořen')),
                ('file', models.ImageField(blank=True, null=True, upload_to=clients.models.signature_directory_path, verbose_name='Obrázek podpisu')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=300, null=True, verbose_name='IP adresa clienta')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to='clients.client', verbose_name='Klient')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'Signatures',
            },
        ),
        migrations.AddIndex(
            model_name='signature',
            index=models.Index(fields=['content_type', 'object_id'], name='clients_sig_content_16121b_idx'),
        ),
    ]

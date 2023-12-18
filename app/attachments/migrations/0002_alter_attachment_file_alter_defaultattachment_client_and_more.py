# Generated by Django 4.2.8 on 2023-12-16 20:50

import attachments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_phone_number'),
        ('proposals', '0002_alter_defaultitem_unit_alter_item_unit'),
        ('attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=attachments.models.attachment_directory_path, verbose_name='soubor'),
        ),
        migrations.AlterField(
            model_name='defaultattachment',
            name='client',
            field=models.ManyToManyField(blank=True, related_name='default_attachments', to='clients.client', verbose_name='klient'),
        ),
        migrations.RemoveField(
            model_name='defaultattachment',
            name='contract_type',
        ),
        migrations.AlterField(
            model_name='defaultattachment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=attachments.models.default_attachment_directory_path, verbose_name='soubor'),
        ),
        migrations.RemoveField(
            model_name='defaultattachment',
            name='subject',
        ),
        migrations.AddField(
            model_name='defaultattachment',
            name='contract_type',
            field=models.ManyToManyField(related_name='default_attachment', to='proposals.contracttype', verbose_name='typ smlouvy'),
        ),
        migrations.AddField(
            model_name='defaultattachment',
            name='subject',
            field=models.ManyToManyField(related_name='default_attachment', to='proposals.contractsubject', verbose_name='předmět smlouvy'),
        ),
    ]
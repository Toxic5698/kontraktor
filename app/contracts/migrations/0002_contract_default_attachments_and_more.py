# Generated by Django 4.2.11 on 2024-03-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_defaultattachment_document_type_and_more'),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='default_attachments',
            field=models.ManyToManyField(related_name='%(class)ss', to='attachments.defaultattachment', verbose_name='Automatické přílohy'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='default_attachments',
            field=models.ManyToManyField(related_name='%(class)ss', to='attachments.defaultattachment', verbose_name='Automatické přílohy'),
        ),
    ]

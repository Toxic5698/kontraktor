# Generated by Django 4.1.3 on 2022-12-15 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_attachment_add_to_contract_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='name',
            new_name='file_name',
        ),
    ]

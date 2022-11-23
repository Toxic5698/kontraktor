# Generated by Django 4.1.3 on 2022-11-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0011_alter_contract_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='corporation',
        ),
        migrations.AddField(
            model_name='contract',
            name='consumer',
            field=models.BooleanField(default=False, verbose_name='Spotřebitel (fyzická osoba)'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Adresa bydliště nebo sídla'),
        ),
    ]

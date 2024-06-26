# Generated by Django 4.2.11 on 2024-03-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Název společnosti')),
                ('address', models.CharField(max_length=256, verbose_name='Sídlo')),
                ('id_number', models.CharField(max_length=9, verbose_name='IČ')),
                ('bank_number', models.CharField(max_length=30, verbose_name='Číslo účtu')),
                ('acting_person', models.CharField(max_length=200, verbose_name='Zastoupená...')),
                ('web', models.CharField(blank=True, max_length=100, null=True, verbose_name='Link operátora')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon')),
            ],
            options={
                'verbose_name': 'Operator',
                'verbose_name_plural': 'Operators',
            },
        ),
    ]

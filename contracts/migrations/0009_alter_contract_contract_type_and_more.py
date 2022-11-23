# Generated by Django 4.1.3 on 2022-11-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0008_contracttype_remove_contract_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_type',
            field=models.ManyToManyField(related_name='contracts', to='contracts.contracttype'),
        ),
        migrations.AlterField(
            model_name='contractcore',
            name='contract',
            field=models.ManyToManyField(related_name='contract_cores', to='contracts.contract'),
        ),
        migrations.AlterField(
            model_name='contractcore',
            name='parent_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

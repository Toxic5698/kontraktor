# Generated by Django 4.1.3 on 2023-06-30 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_rename_sale_price_item_price_per_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='production_data',
            field=models.TextField(blank=True, null=True, verbose_name='výrobní data'),
        ),
    ]

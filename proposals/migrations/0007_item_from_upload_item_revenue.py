# Generated by Django 4.1.3 on 2022-12-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_rename_price_item_production_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='from_upload',
            field=models.BooleanField(default=False, verbose_name='nahraná položka'),
        ),
        migrations.AddField(
            model_name='item',
            name='revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='zisk'),
        ),
    ]

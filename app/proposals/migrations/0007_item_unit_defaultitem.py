# Generated by Django 4.1.3 on 2023-11-01 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_rename_sale_price_item_price_per_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.CharField(blank=True, choices=[('ks', 'Ks'), ('kg', 'Kg'), ('l', 'Liters'), ('mb', 'Cubic Meters'), ('m2', 'Square Meters'), ('hod', 'Hours')], max_length=5, null=True, verbose_name='jednotka'),
        ),
        migrations.CreateModel(
            name='DefaultItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='název')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='popis')),
                ('production_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='nákladová cena za jednotku')),
                ('price_per_unit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='cena ze jednotku')),
                ('unit', models.CharField(blank=True, choices=[('ks', 'Ks'), ('kg', 'Kg'), ('l', 'Liters'), ('mb', 'Cubic Meters'), ('m2', 'Square Meters'), ('hod', 'Hours')], max_length=5, null=True, verbose_name='jednotka')),
                ('contract_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_item', to='proposals.contracttype', verbose_name='typ smlouvy')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_item', to='proposals.contractsubject', verbose_name='předmět smlouvy')),
            ],
            options={
                'verbose_name': 'Default Item',
                'verbose_name_plural': 'Default Items',
            },
        ),
    ]

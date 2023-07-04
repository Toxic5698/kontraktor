# Generated by Django 4.1.3 on 2023-07-04 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_signature_ip'),
        ('proposals', '0007_alter_item_production_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='clients.client', verbose_name='klient'),
        ),
    ]
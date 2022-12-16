# Generated by Django 4.1.3 on 2022-12-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0007_item_from_upload_item_revenue'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadedproposal',
            options={'ordering': ['uploaded_at'], 'verbose_name': 'UploadedProposal', 'verbose_name_plural': 'UploadedProposals'},
        ),
        migrations.AlterField(
            model_name='proposal',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Cena'),
        ),
    ]

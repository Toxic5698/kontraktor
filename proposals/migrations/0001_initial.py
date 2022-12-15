# Generated by Django 4.1.3 on 2022-11-30 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0016_delete_attachment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Číslo nabídky')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořena dne')),
                ('edited_at', models.DateTimeField(blank=True, null=True, verbose_name='Upravena dne')),
                ('signed_at', models.DateTimeField(blank=True, null=True, verbose_name='Podepsána dne')),
                ('subject', models.CharField(blank=True, choices=[('DVERE', 'pouze dveře'), ('PODLAHA', 'pouze podlaha'), ('DVERE_PODLAHA', 'dveře i podlaha'), ('ZBOZI', 'zboží')], max_length=100, null=True, verbose_name='Předmět nabídky')),
                ('price', models.CharField(max_length=20, verbose_name='Cena')),
                ('fulfillment_at', models.DateField(blank=True, null=True, verbose_name='Čas plnění')),
                ('fulfillment_place', models.CharField(max_length=1000, verbose_name='Místo plnění')),
                ('contract_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposals', to='contracts.contracttype', verbose_name='Typ smlouvy')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposal_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Vytvořil')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposal_edited_by', to=settings.AUTH_USER_MODEL, verbose_name='Upravil')),
            ],
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-16 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import proposals.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Číslo nabídky')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořena dne')),
                ('edited_at', models.DateTimeField(blank=True, null=True, verbose_name='Upravena dne')),
                ('signed_at', models.DateTimeField(blank=True, null=True, verbose_name='Potvrzena dne')),
                ('subject', models.CharField(blank=True, choices=[('DVERE', 'pouze dveře'), ('PODLAHA', 'pouze podlaha'), ('DVERE_PODLAHA', 'dveře i podlaha'), ('ZBOZI', 'zboží')], max_length=100, null=True, verbose_name='Předmět nabídky')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Cena')),
                ('fulfillment_at', models.DateField(blank=True, null=True, verbose_name='Čas plnění')),
                ('fulfillment_place', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Místo plnění')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposals', to='clients.client', verbose_name='klient')),
                ('contract_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposals', to='proposals.contracttype', verbose_name='Typ smlouvy')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposal_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Vytvořil')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposal_edited_by', to=settings.AUTH_USER_MODEL, verbose_name='Upravil')),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
            },
        ),
        migrations.CreateModel(
            name='UploadedProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(blank=True, max_length=3, null=True, verbose_name='pořadí')),
                ('file', models.FileField(blank=True, null=True, upload_to=proposals.models.uploaded_proposal_directory_path, verbose_name='Podkladová nabídka')),
                ('file_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='název souboru')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Nahráno dne')),
                ('proposal', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded', to='proposals.proposal', verbose_name='nabídka')),
            ],
            options={
                'verbose_name': 'UploadedProposal',
                'verbose_name_plural': 'UploadedProposals',
                'ordering': ['uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='výše')),
                ('part', models.IntegerField(verbose_name='část z celku')),
                ('due', models.CharField(choices=[('10', 'po podpisu smlouvy'), ('21', 'před dodáním'), ('31', 'po dodání'), ('32', 'po dokončení'), ('22', 'před dokončením'), ('99', '-')], default='99', max_length=100, verbose_name='splatnost')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='proposals.proposal', verbose_name='nabídka')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ['due'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(blank=True, null=True, verbose_name='pořadí')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='název')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='popis')),
                ('production_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='cena')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='cena')),
                ('sale_discount', models.IntegerField(blank=True, null=True, verbose_name='sleva')),
                ('revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='zisk')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='množství')),
                ('production_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='výrobní termín')),
                ('production_data', models.CharField(blank=True, max_length=1000, null=True, verbose_name='výrobní data')),
                ('from_upload', models.BooleanField(default=False, verbose_name='nahraná položka')),
                ('proposal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='proposals.proposal', verbose_name='nabídka')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'ordering': ['priority'],
            },
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-07 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('contracts', '0016_delete_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='address',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='id_number',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='note',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='clients.client'),
        ),
    ]
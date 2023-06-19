# Generated by Django 4.1.3 on 2023-06-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_alter_attachment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='purpose',
            field=models.CharField(blank=True, choices=[('intern', 'intern'), ('proposal', 'proposal'), ('contract', 'contract'), ('both', 'both'), ('protocol', 'protocol')], max_length=10, null=True),
        ),
    ]

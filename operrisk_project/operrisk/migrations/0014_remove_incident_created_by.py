# Generated by Django 2.1.2 on 2018-10-23 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0013_auto_20181023_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='created_by',
        ),
    ]

# Generated by Django 2.1.2 on 2018-11-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0018_auto_20181105_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='name',
            field=models.CharField(max_length=256, verbose_name='full name'),
        ),
    ]

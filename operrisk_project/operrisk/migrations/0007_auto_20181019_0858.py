# Generated by Django 2.1.2 on 2018-10-19 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0006_incident_att'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='att',
            field=models.FileField(blank=True, null=True, upload_to='files_att'),
        ),
    ]
# Generated by Django 2.0.5 on 2018-10-18 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0002_auto_20181016_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='URL_name',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='incident',
            name='loss_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='measures_taken',
            field=models.CharField(default='', max_length=2048),
        ),
    ]

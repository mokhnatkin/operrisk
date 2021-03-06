# Generated by Django 2.1.2 on 2018-11-05 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0020_auto_20181105_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='att',
            field=models.FileField(blank=True, null=True, upload_to='files_att/'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operrisk.Category'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='incident',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='description',
            field=models.CharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='incident',
            name='loss_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='measures_taken',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='incident',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]

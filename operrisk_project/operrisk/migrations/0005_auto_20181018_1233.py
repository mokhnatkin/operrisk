# Generated by Django 2.1.2 on 2018-10-18 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operrisk', '0004_auto_20181018_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='caterogy_id',
            new_name='category_id',
        ),
    ]
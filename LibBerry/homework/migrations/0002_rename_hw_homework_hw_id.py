# Generated by Django 4.0.1 on 2022-05-14 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='hw',
            new_name='hw_id',
        ),
    ]

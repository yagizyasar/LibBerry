# Generated by Django 4.0.1 on 2022-05-03 23:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0009_alter_mainuser_registrar_id_alter_mainuser_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='registrar_id',
            field=models.ForeignKey(blank=True, db_column='registrar_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrar_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='outsidemember',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 4, 2, 11, 44, 262879)),
        ),
    ]

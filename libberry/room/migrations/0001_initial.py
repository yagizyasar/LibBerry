# Generated by Django 4.0.1 on 2022-04-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Private_Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('capacity', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=10)),
            ],
        ),
    ]

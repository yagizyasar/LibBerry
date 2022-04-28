# Generated by Django 4.0.1 on 2022-04-28 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=32)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=7)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('registrar_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('office', models.CharField(max_length=8)),
                ('department', models.CharField(max_length=4)),
                ('tenure', models.CharField(choices=[('Prof', 'Professor'), ('Assoc. Prof', 'Assoc Prof'), ('Asst. Prof', 'Asst Prof'), ('Inst', 'Instructor')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('specialization', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='OutsideMember',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('card_no', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('department', models.CharField(max_length=16)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
    ]

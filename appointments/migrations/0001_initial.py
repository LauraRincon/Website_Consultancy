# Generated by Django 3.1.2 on 2020-11-05 05:11

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=20)),
                ('enterprise', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('place', models.CharField(default='', max_length=30)),
                ('billing', models.CharField(default='', max_length=15)),
                ('category', models.CharField(choices=[('Residential', 'Residential'), ('Comertial', 'Comertial'), ('Industrial', 'Industrial'), ('Medium Voltage Industrial', 'Medium Voltage Industrial'), ('Large Scale', 'Large Scale')], max_length=50)),
                ('appt_date', models.DateTimeField(verbose_name='appointment date')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='appointments.user')),
            ],
        ),
    ]

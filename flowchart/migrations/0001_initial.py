# Generated by Django 3.2 on 2022-09-05 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('incident_number', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Flowchart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('primary', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowchart.location')),
            ],
            options={
                'unique_together': {('name', 'location')},
            },
        ),
    ]

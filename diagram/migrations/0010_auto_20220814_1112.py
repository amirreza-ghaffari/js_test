# Generated by Django 3.2 on 2022-08-14 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagram', '0009_auto_20220814_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='figure',
            field=models.CharField(blank=True, choices=[('Procedure', 'Procedure'), ('Cylinder1', 'Cylinder1'), ('Terminator', 'Terminator'), ('CreateRequest', 'CreateRequest'), ('Document', 'Document'), ('Diamond', 'Diamond')], default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='historicalblock',
            name='figure',
            field=models.CharField(blank=True, choices=[('Procedure', 'Procedure'), ('Cylinder1', 'Cylinder1'), ('Terminator', 'Terminator'), ('CreateRequest', 'CreateRequest'), ('Document', 'Document'), ('Diamond', 'Diamond')], default=None, max_length=256, null=True),
        ),
    ]

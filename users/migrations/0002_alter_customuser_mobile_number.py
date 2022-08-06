# Generated by Django 3.2.6 on 2022-08-02 13:40

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(max_length=11, null=True, validators=[users.models.validate_phone_number]),
        ),
    ]

# Generated by Django 3.2 on 2022-09-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_rand_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rand_text',
            field=models.CharField(default=None, max_length=16, null=True),
        ),
    ]
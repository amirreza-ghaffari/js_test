# Generated by Django 3.2.6 on 2022-08-03 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220803_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='department',
            field=models.CharField(choices=[('Legal', 'Legal'), ('Risk Audit Compliance', 'RAC'), ('Human Recourse', 'HR'), ('Marketing', 'Marketing'), ('Technology', 'Tech'), ('Finance', 'Finance'), ('User Experience', 'User Experience'), ('Financial', 'Financial'), ('Business Development', 'Business Development'), ('Operation', 'Operation')], max_length=256, null=True),
        ),
    ]

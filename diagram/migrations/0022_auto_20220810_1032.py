# Generated by Django 3.2 on 2022-08-10 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('diagram', '0021_block_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalblock',
            name='user_groups',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group'),
        ),
        migrations.RemoveField(
            model_name='block',
            name='user_groups',
        ),
        migrations.AddField(
            model_name='block',
            name='user_groups',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]

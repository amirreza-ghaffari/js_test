# Generated by Django 3.2 on 2022-09-10 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagram', '0005_auto_20220907_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='end_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_transition', to='diagram.block'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='start_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_transition', to='diagram.block'),
        ),
    ]
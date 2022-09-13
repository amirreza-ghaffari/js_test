# Generated by Django 3.2 on 2022-09-10 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagram', '0006_auto_20220910_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='end_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_transition', to='diagram.block'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='start_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_transition', to='diagram.block'),
        ),
    ]

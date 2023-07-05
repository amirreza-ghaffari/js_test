# Generated by Django 3.2 on 2023-07-05 18:13

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import flowchart.models
import flowchart.storage
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContingencyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developed', models.PositiveIntegerField(default=0)),
                ('in_progress', models.PositiveIntegerField(default=0)),
                ('not_developed', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Flowchart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('primary', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('triggered_date', models.DateTimeField(blank=True, null=True)),
                ('incident_counter', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(storage=flowchart.storage.OverwriteStorage, upload_to=flowchart.models.screenshot_path)),
                ('flowchart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='screenshot', to='flowchart.flowchart')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_history', jsonfield.fields.JSONField(default=dict)),
                ('block_history', jsonfield.fields.JSONField(default=dict)),
                ('email_response', jsonfield.fields.JSONField(default=dict)),
                ('initial_date', models.DateTimeField()),
                ('j_initial_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('flowchart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowchart.flowchart')),
            ],
        ),
        migrations.AddField(
            model_name='flowchart',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowchart.location'),
        ),
        migrations.CreateModel(
            name='CrisisSeverityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(storage=flowchart.storage.OverwriteStorage, upload_to=flowchart.models.severity_path)),
                ('flowchart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_query_name='severity_image', to='flowchart.flowchart')),
            ],
            options={
                'verbose_name': 'Crisis Image',
                'verbose_name_plural': 'Crisis Images',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flowchart',
            unique_together={('name', 'location')},
        ),
    ]

# Generated by Django 3.1 on 2020-09-13 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='image',
        ),
        migrations.RemoveField(
            model_name='recommendationtouser',
            name='is_complete',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recommendation_link',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='recommendationtouser',
            name='snooze_interval',
            field=models.DurationField(default=datetime.timedelta(0)),
            preserve_default=False,
        ),
    ]
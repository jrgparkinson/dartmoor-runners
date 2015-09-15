# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0029_result_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='lat',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='lon',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0021_auto_20150903_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='new_time',
            field=models.DurationField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_event_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='year',
            field=models.IntegerField(default=1900),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0012_series_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='new_number',
            field=models.IntegerField(default=-1),
        ),
    ]

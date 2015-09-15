# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0022_result_new_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='time',
        ),
    ]

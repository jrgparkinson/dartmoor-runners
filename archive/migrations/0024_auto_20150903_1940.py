# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0023_remove_result_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='new_time',
            new_name='time',
        ),
    ]

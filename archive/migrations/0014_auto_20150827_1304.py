# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0013_event_new_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='number',
            new_name='old_number',
        ),
    ]

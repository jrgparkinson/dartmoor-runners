# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0014_auto_20150827_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='new_number',
            new_name='number',
        ),
    ]

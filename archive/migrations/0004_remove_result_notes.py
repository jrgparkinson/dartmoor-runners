# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20150824_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='notes',
        ),
    ]

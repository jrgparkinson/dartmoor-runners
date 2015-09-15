# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0026_auto_20150911_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='position',
            field=models.FloatField(default=999),
        ),
    ]

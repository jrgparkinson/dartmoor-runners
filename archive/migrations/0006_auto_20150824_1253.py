# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20150824_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]

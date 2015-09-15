# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0025_auto_20150911_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='position',
            field=models.IntegerField(default=999),
        ),
        migrations.AlterField(
            model_name='event',
            name='gridref',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
    ]

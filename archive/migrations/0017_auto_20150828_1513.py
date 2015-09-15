# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0016_auto_20150828_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultdatatype',
            name='type',
            field=models.CharField(max_length=20, choices=[('time', 'Time'), ('score', 'Score')], default='time'),
        ),
    ]

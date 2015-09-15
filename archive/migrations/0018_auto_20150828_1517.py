# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0017_auto_20150828_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='type',
            field=models.ForeignKey(to='archive.ResultDataType', default=1),
        ),
    ]

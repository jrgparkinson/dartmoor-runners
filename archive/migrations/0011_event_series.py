# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0010_auto_20150826_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.ForeignKey(to='archive.Series', default=-1),
        ),
    ]

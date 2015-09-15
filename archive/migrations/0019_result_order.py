# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0018_auto_20150828_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]

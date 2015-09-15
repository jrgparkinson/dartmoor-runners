# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0028_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='points',
            field=models.FloatField(default=None, blank=True, null=True),
        ),
    ]

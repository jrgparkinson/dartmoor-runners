# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0019_result_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='number_increment',
            field=models.IntegerField(default=1),
        ),
    ]

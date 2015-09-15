# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0007_auto_20150824_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(null=True),
        ),
    ]

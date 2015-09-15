# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_remove_result_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='result',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]

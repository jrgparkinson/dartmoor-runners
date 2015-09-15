# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_auto_20150824_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='event',
            name='organisers',
        ),
        migrations.AddField(
            model_name='event',
            name='organisers',
            field=models.ManyToManyField(to='archive.Runner'),
        ),
    ]

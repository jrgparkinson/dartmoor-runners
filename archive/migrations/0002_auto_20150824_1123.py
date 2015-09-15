# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='result',
            old_name='runner_id',
            new_name='runner',
        ),
        migrations.AddField(
            model_name='event',
            name='number',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='result',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='time',
            field=models.DateTimeField(verbose_name='00:00:00'),
        ),
    ]

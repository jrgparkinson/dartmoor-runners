# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0024_auto_20150903_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='runner',
            options={'ordering': ['surname']},
        ),
        migrations.AddField(
            model_name='event',
            name='source',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='notes',
            field=models.TextField(default='', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='runner',
            name='sex',
            field=models.CharField(default='U', choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='series',
            name='season',
            field=models.CharField(default='Winter', choices=[('Winter', 'Winter'), ('Summer', 'Summer')], max_length=20),
        ),
    ]

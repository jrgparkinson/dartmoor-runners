# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0009_auto_20150824_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=-1)),
                ('season', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='series',
            new_name='series_number',
        ),
    ]

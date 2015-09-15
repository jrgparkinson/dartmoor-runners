# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('organisers', models.CharField(max_length=255)),
                ('gridref', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Running time')),
                ('competitive', models.BooleanField(default=True)),
                ('notes', models.CharField(max_length=2000)),
                ('event_id', models.ForeignKey(to='archive.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('sex', models.CharField(max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='runner_id',
            field=models.ForeignKey(to='archive.Runner'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0015_auto_20150827_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultDataType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('short_description', models.CharField(max_length=50)),
                ('long_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AddField(
            model_name='result',
            name='type',
            field=models.ForeignKey(default=0, to='archive.ResultDataType'),
        ),
    ]

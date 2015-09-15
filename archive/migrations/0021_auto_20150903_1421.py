# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0020_event_number_increment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=500)),
                ('event', models.ForeignKey(to='archive.Event')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='course',
            field=models.ForeignKey(to='archive.Course', default=None, null=True, blank=True),
        ),
    ]

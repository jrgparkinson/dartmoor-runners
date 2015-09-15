# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0027_auto_20150911_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('firstname', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('runner', models.ForeignKey(to='archive.Runner')),
            ],
        ),
    ]

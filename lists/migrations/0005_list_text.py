# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='text',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]

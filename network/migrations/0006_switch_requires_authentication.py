# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20141011_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='requires_authentication',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]

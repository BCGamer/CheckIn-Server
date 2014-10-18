# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkcontrol', '0003_auto_20141011_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]

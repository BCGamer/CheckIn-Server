# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20150117_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='email address'),
        ),
    ]

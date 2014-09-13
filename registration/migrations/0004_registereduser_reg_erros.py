# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_remove_registereduser_shared_file_print_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='reg_erros',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]

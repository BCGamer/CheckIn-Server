# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_remove_responsecode_windows_setting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registereduser',
            name='shared_file_print_off',
        ),
    ]

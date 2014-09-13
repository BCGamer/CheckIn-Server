# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_registereduser_reg_erros'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registereduser',
            old_name='reg_erros',
            new_name='reg_errors',
        ),
    ]

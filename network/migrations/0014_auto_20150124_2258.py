# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20150124_2250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vlan',
            old_name='vlan_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='vlan',
            old_name='vlan_num',
            new_name='num',
        ),
        migrations.RenameField(
            model_name='vlan',
            old_name='vlan_type',
            new_name='type',
        ),
    ]

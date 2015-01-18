# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20150117_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='UplinkPort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.IntegerField()),
                ('switch', models.ForeignKey(to='network.Switch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='uplinkport',
            unique_together=set([('port', 'switch')]),
        ),
    ]

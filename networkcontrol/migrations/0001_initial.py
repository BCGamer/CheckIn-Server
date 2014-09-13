# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('ip', models.GenericIPAddressField()),
                ('type', models.CharField(default=b'hp', max_length=20, choices=[(b'hp', b'HP'), (b'cisco', b'Cisco')])),
            ],
            options={
                'verbose_name_plural': 'Switches',
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorylane', '0007_auto_20151206_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='first_name',
            field=models.CharField(default=b'Memory', max_length=100),
        ),
        migrations.AddField(
            model_name='memory',
            name='last_name',
            field=models.CharField(default=b'Lane', max_length=100),
        ),
    ]

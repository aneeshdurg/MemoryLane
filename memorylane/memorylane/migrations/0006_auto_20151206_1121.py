# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorylane', '0005_userprofile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=b'Default bio'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='propic',
            field=models.FileField(upload_to=b'memorylane/static/images/profile'),
        ),
    ]

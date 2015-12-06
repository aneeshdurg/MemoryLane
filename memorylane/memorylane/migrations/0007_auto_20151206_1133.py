# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorylane', '0006_auto_20151206_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='author_image',
            field=models.FileField(default=b'memorylane/static/user-images/Default.png', upload_to=b''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.FileField(default=b'memorylane/static/user-images/Default.png', upload_to=b'memorylane/static/user-images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='livesin',
            field=models.TextField(default=b'Earth'),
        ),
    ]

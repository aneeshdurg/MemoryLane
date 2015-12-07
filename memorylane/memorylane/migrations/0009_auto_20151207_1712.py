# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorylane', '0008_auto_20151206_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=5000)),
                ('photo', models.FileField(upload_to=b'memorylane/static/images')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='memory',
            name='lat',
            field=models.CharField(default=0, max_length=5000),
        ),
        migrations.AddField(
            model_name='memory',
            name='lng',
            field=models.CharField(default=0, max_length=5000),
        ),
    ]

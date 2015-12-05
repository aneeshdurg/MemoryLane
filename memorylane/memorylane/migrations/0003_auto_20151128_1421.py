# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorylane', '0002_auto_20151007_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=5000)),
                ('friends', models.CharField(max_length=5000)),
                ('propic', models.CharField(max_length=1000)),
                ('date_created', models.DateField()),
                ('bio', models.TextField()),
                ('memories', models.CharField(max_length=5000)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='memory',
            name='image',
            field=models.FileField(upload_to=b'memorylane/static/images'),
        ),
    ]

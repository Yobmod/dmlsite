# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-01 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmlblog', '0004_auto_20170201_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=True),
        ),
    ]

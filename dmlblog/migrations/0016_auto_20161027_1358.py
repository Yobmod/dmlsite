# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmlblog', '0015_auto_20161027_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='height_field',
            new_name='image_height',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to='/'),
        ),
    ]
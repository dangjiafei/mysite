# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-30 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.IntegerField(default=11),
            preserve_default=False,
        ),
    ]

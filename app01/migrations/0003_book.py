# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-29 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_press'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Press')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-05 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Phone', '0007_auto_20170605_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='Android_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Phone.Android'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='iOS_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Phone.iOS'),
        ),
    ]

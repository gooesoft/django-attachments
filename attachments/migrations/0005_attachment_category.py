# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-26 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0004_attachment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='category',
            field=models.CharField(choices=[('', ''), ('INVOICE', 'Invoice'), ('RECEIPT', 'Receipt')], default='', max_length=30),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 10:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guest',
            options={'verbose_name': '嘉宾', 'verbose_name_plural': '嘉宾'},
        ),
        migrations.RenameField(
            model_name='guest',
            old_name='e_mail',
            new_name='p_e_mail',
        ),
        migrations.RenameField(
            model_name='guest',
            old_name='pname',
            new_name='p_name',
        ),
        migrations.RenameField(
            model_name='guest',
            old_name='sign',
            new_name='p_sign',
        ),
        migrations.RenameField(
            model_name='guest',
            old_name='sign_time',
            new_name='p_sign_time',
        ),
    ]
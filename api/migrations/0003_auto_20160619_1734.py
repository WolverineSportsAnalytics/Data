# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rotowire_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='RotogrindersBatters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('position', models.CharField(max_length=3)),
                ('secondaryPosition', models.CharField(max_length=3)),
                ('salary', models.CharField(max_length=10)),
                ('team', models.CharField(max_length=15)),
                ('opponent', models.CharField(max_length=250)),
                ('bats', models.CharField(max_length=5)),
                ('ceiling', models.CharField(max_length=10)),
                ('floor', models.CharField(max_length=10)),
                ('projPoints', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=10)),
                ('pitcherName', models.CharField(max_length=250)),
                ('pitcherThrows', models.CharField(max_length=5)),
                ('seasonAB', models.CharField(max_length=7)),
                ('average', models.CharField(max_length=7)),
                ('wOBA', models.CharField(max_length=7)),
                ('ISO', models.CharField(max_length=7)),
                ('OBP', models.CharField(max_length=7)),
                ('BABIP', models.CharField(max_length=7)),
                ('SLG', models.CharField(max_length=7)),
                ('kPercentage', models.CharField(max_length=7)),
                ('BB', models.CharField(max_length=7)),
                ('OPS', models.CharField(max_length=7)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RotogrindersData', to='api.TimeKeeper')),
            ],
        ),
        migrations.AlterField(
            model_name='rotowire',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RotowireData', to='api.TimeKeeper'),
        ),
    ]

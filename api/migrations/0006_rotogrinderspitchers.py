# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160619_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='RotogrindersPitchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('position', models.CharField(blank=True, max_length=3, null=True)),
                ('salary', models.CharField(blank=True, max_length=10, null=True)),
                ('team', models.CharField(blank=True, max_length=5, null=True)),
                ('opponent', models.CharField(blank=True, max_length=5, null=True)),
                ('playerThrows', models.CharField(blank=True, max_length=5, null=True)),
                ('ceiling', models.CharField(blank=True, max_length=10, null=True)),
                ('floor', models.CharField(blank=True, max_length=10, null=True)),
                ('projPoints', models.CharField(blank=True, max_length=10, null=True)),
                ('value', models.CharField(blank=True, max_length=10, null=True)),
                ('xISO', models.CharField(blank=True, max_length=7, null=True)),
                ('xR', models.CharField(blank=True, max_length=7, null=True)),
                ('xSLG', models.CharField(blank=True, max_length=7, null=True)),
                ('xWOBA', models.CharField(blank=True, max_length=7, null=True)),
                ('xL', models.CharField(blank=True, max_length=7, null=True)),
                ('GP', models.CharField(blank=True, max_length=7, null=True)),
                ('lWOBA', models.CharField(blank=True, max_length=7, null=True)),
                ('rWOBA', models.CharField(blank=True, max_length=7, null=True)),
                ('lSLG', models.CharField(blank=True, max_length=7, null=True)),
                ('rSLG', models.CharField(blank=True, max_length=7, null=True)),
                ('SIERA', models.CharField(blank=True, max_length=7, null=True)),
                ('xFIP', models.CharField(blank=True, max_length=7, null=True)),
                ('lISO', models.CharField(blank=True, max_length=7, null=True)),
                ('rISO', models.CharField(blank=True, max_length=7, null=True)),
                ('GBPercentage', models.CharField(blank=True, max_length=7, null=True)),
                ('FBPercentage', models.CharField(blank=True, max_length=7, null=True)),
                ('IP', models.CharField(blank=True, max_length=7, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RotogrindersPitchersData', to='api.TimeKeeper')),
            ],
        ),
    ]
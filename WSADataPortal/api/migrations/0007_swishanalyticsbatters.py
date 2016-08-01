# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rotogrinderspitchers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwishAnalyticsBatters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('salary', models.CharField(blank=True, max_length=10, null=True)),
                ('bats', models.CharField(blank=True, max_length=5, null=True)),
                ('position', models.CharField(blank=True, max_length=5, null=True)),
                ('team', models.CharField(blank=True, max_length=250, null=True)),
                ('opponent', models.CharField(blank=True, max_length=250, null=True)),
                ('projPoints', models.CharField(blank=True, max_length=7, null=True)),
                ('value', models.CharField(blank=True, max_length=7, null=True)),
                ('outs', models.CharField(blank=True, max_length=7, null=True)),
                ('AB', models.CharField(blank=True, max_length=7, null=True)),
                ('BB', models.CharField(blank=True, max_length=7, null=True)),
                ('HBP', models.CharField(blank=True, max_length=7, null=True)),
                ('singles', models.CharField(blank=True, max_length=7, null=True)),
                ('doubles', models.CharField(blank=True, max_length=7, null=True)),
                ('triples', models.CharField(blank=True, max_length=7, null=True)),
                ('HR', models.CharField(blank=True, max_length=7, null=True)),
                ('RBI', models.CharField(blank=True, max_length=7, null=True)),
                ('SB', models.CharField(blank=True, max_length=7, null=True)),
                ('CS', models.CharField(blank=True, max_length=7, null=True)),
                ('averageDKPoints', models.CharField(blank=True, max_length=7, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SwishAnalyticsBatters', to='api.TimeKeeper')),
            ],
        ),
    ]
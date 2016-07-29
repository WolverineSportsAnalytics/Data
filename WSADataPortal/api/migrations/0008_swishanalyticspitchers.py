# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 02:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_swishanalyticsbatters'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwishAnalyticsPitchers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('salary', models.CharField(blank=True, max_length=10, null=True)),
                ('team', models.CharField(blank=True, max_length=250, null=True)),
                ('opponent', models.CharField(blank=True, max_length=250, null=True)),
                ('projPoints', models.CharField(blank=True, max_length=7, null=True)),
                ('value', models.CharField(blank=True, max_length=7, null=True)),
                ('outs', models.CharField(blank=True, max_length=7, null=True)),
                ('ER', models.CharField(blank=True, max_length=7, null=True)),
                ('Hits', models.CharField(blank=True, max_length=7, null=True)),
                ('Walks', models.CharField(blank=True, max_length=7, null=True)),
                ('HBP', models.CharField(blank=True, max_length=7, null=True)),
                ('Ks', models.CharField(blank=True, max_length=7, null=True)),
                ('CG', models.CharField(blank=True, max_length=7, null=True)),
                ('CGSO', models.CharField(blank=True, max_length=7, null=True)),
                ('NOHit', models.CharField(blank=True, max_length=7, null=True)),
                ('Win', models.CharField(blank=True, max_length=7, null=True)),
                ('averageDKPoints', models.CharField(blank=True, max_length=7, null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SwishAnalyticsPitchers', to='api.TimeKeeper')),
            ],
        ),
    ]

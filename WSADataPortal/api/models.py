from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	create = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=20)

class TimeKeeper(models.Model):
	name = models.CharField(max_length=250)
	scraped = models.DateTimeField(auto_now_add=True)

class Rotowire(models.Model):
	parent = models.ForeignKey(TimeKeeper, related_name='RotowireData')
	name = models.CharField(max_length=250)
	bats = models.CharField(max_length=250)
	team = models.CharField(max_length=250, default='WSA')
	position = models.CharField(max_length=250)
	orderInLU = models.CharField(max_length=250)
	opponent = models.CharField(max_length=250)
	opponentThrows = models.CharField(max_length=250)
	salary = models.CharField(max_length=250)
	projPoints = models.CharField(max_length=250)
	ceiling = models.CharField(max_length=250)
	floor = models.CharField(max_length=250)
	value = models.CharField(max_length=250)
	moneyLine = models.CharField(max_length=250)
	overUnder = models.CharField(max_length=250)

class RotogrindersBatters(models.Model):
	parent = models.ForeignKey(TimeKeeper, related_name='RotogrindersData')
	name = models.CharField(max_length=250, blank=True, null=True)
	position = models.CharField(max_length=3, blank=True, null=True)
	secondaryPosition = models.CharField(max_length=3, blank=True, null=True)
	salary = models.CharField(max_length=10, blank=True, null=True)
	team = models.CharField(max_length=15, blank=True, null=True)
	opponent = models.CharField(max_length=250, blank=True, null=True)
	bats = models.CharField(max_length=5, blank=True, null=True)
	ceiling = models.CharField(max_length=10, blank=True, null=True)
	floor = models.CharField(max_length=10, blank=True, null=True)
	projPoints = models.CharField(max_length=10, blank=True, null=True)
	value = models.CharField(max_length=10, blank=True, null=True)
	pitcherName = models.CharField(max_length=250, null=True, blank=True)
	pitcherThrows = models.CharField(max_length=5, blank=True, null=True)
	seasonAB = models.CharField(max_length=7, blank=True, null=True)
	average = models.CharField(max_length=7, blank=True, null=True)
	wOBA = models.CharField(max_length=7, blank=True, null=True)
	ISO = models.CharField(max_length=7, blank=True, null=True)
	OBP = models.CharField(max_length=7, blank=True, null=True)
	BABIP = models.CharField(max_length=7, blank=True, null=True)
	SLG = models.CharField(max_length=7, blank=True, null=True)
	kPercentage = models.CharField(max_length=7, blank=True, null=True)
	BB = models.CharField(max_length=7, blank=True, null=True)
	OPS = models.CharField(max_length=7, blank=True, null=True)


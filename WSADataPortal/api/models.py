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
	parent = models.ForeignKey(TimeKeeper, related_name='data')
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


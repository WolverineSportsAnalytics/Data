from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	create = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=20)


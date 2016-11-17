from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
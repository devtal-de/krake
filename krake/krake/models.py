from django.db import models

# Create your models here.

class foreignSystem(models.Model):
    name = models.CharField(max_length=200)

class Owner(models.Model):
    name = models.CharField(max_length=200)


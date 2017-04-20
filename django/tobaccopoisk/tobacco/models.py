from django.db import models

# Create your models here.

class Tobacco(models.Model):
	brand = models.CharField(max_length=20)
	name = models.CharField(max_length=30)
	release_date = models.DateField(auto_now_add=True, null=True)
	description = models.TextField(null=True)
	strength = models.FloatField(null=True)
	smoke = models.FloatField(null=True)
	taste = models.FloatField(null=True)
	heat = models.FloatField(null=True)
	rating = models.FloatField(null=True)
	image = models.ImageField(null=True)

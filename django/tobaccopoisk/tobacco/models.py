from django.db import models

# ----------------
# Start of routine
# ----------------
# This routine is for handling dynamic ImageField
# According to https://code.djangoproject.com/ticket/22999

from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):

	def __init__(self, sub_path):
		self.path = sub_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		filename = instance.brand + '_' + instance.name + '.' + ext
		return self.path + filename

path_and_rename = PathAndRename("tobacco/static/tobacco/")

# --------------
# End of routine
# --------------

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
	image = models.ImageField(null=True, upload_to=path_and_rename)

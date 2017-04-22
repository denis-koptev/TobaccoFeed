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

		# if some bugs would be detected change to
		# return os.path.join(self.path, filename)
		return self.path + filename

path_and_rename = PathAndRename("tobacco/static/tobacco/")

# --------------
# End of routine
# --------------

class Tobacco(models.Model):
	brand = models.CharField(max_length=20)
	name = models.CharField(max_length=30)
	release_date = models.DateField(auto_now_add=True, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	strength = models.FloatField(null=True, blank=True)
	smoke = models.FloatField(null=True, blank=True)
	taste = models.FloatField(null=True, blank=True)
	heat = models.FloatField(null=True, blank=True)
	rating = models.FloatField(null=True, blank=True)
	# create image name according to object brand and model
	image = models.ImageField(null=True, blank=True, upload_to=path_and_rename)

	def __str__(self):
		return self.brand.title() + ' ' +self.name.title()
from django.db import models
from django.conf import settings

# ------------------------
# Create storage to change url path
# 	and delete old file before uploading new one
# ------------------------ 

from django.core.files.storage import FileSystemStorage
import os, re

class TobaccoStorage(FileSystemStorage):

	def get_available_name(self, name, max_length=None):

		# get dir and name_root
		dir_name, file_name = os.path.split(name)
		file_root, file_ext = os.path.splitext(file_name)

		absolute_dir_path = os.path.join(settings.BASE_DIR, dir_name)
		# create pattern like "name_root.*" for all ext
		pattern = file_root + '.*'

		# delete file with name_root recursively
		for f in os.listdir(absolute_dir_path):
			if re.search(pattern, f):
				os.remove(os.path.join(absolute_dir_path, f))

		# return unchanged name
		return name


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

path_and_rename = PathAndRename("tobacco/static/tobacco/tobaccos/")

# --------------
# End of routine
# --------------

EMPTY_TOBACCO = "tobacco/static/tobacco/tobaccos/empty_tobacco.png"

class Tobacco(models.Model):
	brand = models.CharField(max_length=20)
	name = models.CharField(max_length=30)
	release_date = models.DateField(auto_now_add=True, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	strength = models.FloatField(null=True, blank=True)
	strength_votes = models.IntegerField(default=0)
	smoke = models.FloatField(null=True, blank=True)
	smoke_votes = models.IntegerField(default=0)
	taste = models.FloatField(null=True, blank=True)
	taste_votes = models.IntegerField(default=0)
	heat = models.FloatField(null=True, blank=True)
	heat_votes = models.IntegerField(default=0)
	rating = models.FloatField(null=True, blank=True)
	rating_votes = models.IntegerField(default=0)
	# create image name according to object brand and model
	image = models.ImageField(null=True, storage=TobaccoStorage(), upload_to=path_and_rename, default=EMPTY_TOBACCO)

	def __str__(self):
		return self.brand.title() + ' ' +self.name.title()

# ----------------
# Start of routine
# 	for signal receivers
# ----------------

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from tobaccopoisk import utils

@receiver(pre_delete, sender=Tobacco)
def tobacco_delete(sender, instance, **kwargs):
	# dont delete empty_tobacco image
	if instance.image.name != EMPTY_TOBACCO:
		instance.image.delete(False)

@receiver(pre_save, sender=Tobacco)
def tobacco_save(sender, instance, **kwargs):
	instance.brand = utils.to_db_str(instance.brand)
	instance.name = utils.to_db_str(instance.name)

# --------------
# End of routine
#	for signal receivers
# --------------


# --------
# Start of
# 	Mixes
# --------

from tobaccopoisk.utils import to_view_str

class Mix(models.Model):
	description = models.TextField(null=True, blank=True)
	rating = models.FloatField(null=True, blank=True)
	rating_votes = models.IntegerField(null=True, default=0)
	pub_date = models.DateField(auto_now_add=True, null=True, blank=True)
	tobaccos = models.ManyToManyField(Tobacco, related_name='mixes')

	def __str__(self):
		return " + ".join(to_view_str(t.brand) + ' ' + to_view_str(t.name) for t in self.tobaccos.all())

	class Meta:
		# The default ordering for the object, 
		# 	for use when obtaining lists of objects:
		ordering = ('-pub_date',)

		# Custom multiple name
		verbose_name_plural = 'Mixes'

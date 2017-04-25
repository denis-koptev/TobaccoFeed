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

class Tobacco(models.Model):
	brand = models.CharField(max_length=20)
	name = models.CharField(max_length=30)
	release_date = models.DateField(auto_now_add=True, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	strength = models.FloatField(null=True, blank=True)
	strength_votes = models.IntegerField(null=True, default=0)
	smoke = models.FloatField(null=True, blank=True)
	smoke_votes = models.IntegerField(null=True, default=0)
	taste = models.FloatField(null=True, blank=True)
	taste_votes = models.IntegerField(null=True, default=0)
	heat = models.FloatField(null=True, blank=True)
	heat_votes = models.IntegerField(null=True, default=0)
	rating = models.FloatField(null=True, blank=True)
	rating_votes = models.IntegerField(null=True, default=0)
	# create image name according to object brand and model
	image = models.ImageField(null=True, storage=TobaccoStorage(), upload_to=path_and_rename, default="tobacco/static/tobacco/tobaccos/empty_tobacco.png")

	def __str__(self):
		return self.brand.title() + ' ' +self.name.title()
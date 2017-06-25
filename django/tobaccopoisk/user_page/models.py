from django.db import models
from auth_page.models import User as AuthUser
from django.conf import settings


from django.core.files.storage import FileSystemStorage
import os, re


class AvatarStorage(FileSystemStorage):

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

from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):

	def __init__(self, sub_path):
		self.path = sub_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		filename = instance.auth_id.login + '.' + ext

		# if some bugs would be detected change to
		# return os.path.join(self.path, filename)
		return self.path + filename

path_and_rename = PathAndRename("user_page/static/user_page/avatars/")

# --------------
# End of routine
# --------------

DEFAULT_AVATAR = "user_page/static/user_page/avatars/default_avatar.svg"

class User(models.Model):
	auth_id = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(null=True, blank=True, max_length=50)
	b_date = models.DateField(null=True, blank=True)
	place = models.CharField(null=True, blank=True, max_length=50)
	avatar = models.ImageField(null=True, blank=True, storage=AvatarStorage(), upload_to=path_and_rename)

	def __str__(self):
		return self.auth_id.login
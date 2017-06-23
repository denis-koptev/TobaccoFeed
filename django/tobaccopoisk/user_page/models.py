from django.db import models
from auth_page.models import User as AuthUser

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
	avatar = models.ImageField(null=True, blank=True, upload_to=path_and_rename)

	def __str__(self):
		return self.auth_id.login
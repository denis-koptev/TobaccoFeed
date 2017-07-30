from django.db import models
from auth_page.models import User as AuthUser
from django.conf import settings
from tobacco_page.models import Tobacco, Mix


from django.core.files.storage import FileSystemStorage
import os, re
from tobaccopoisk import utils

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
	auth_id = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True, related_name='info')
	name = models.CharField(null=True, blank=True, max_length=50)
	b_date = models.DateField(null=True, blank=True)
	place = models.CharField(null=True, blank=True, max_length=50)
	avatar = models.ImageField(null=True, blank=True, storage=AvatarStorage(), upload_to=path_and_rename)

	def __str__(self):
		return self.auth_id.login

	class Meta:
		verbose_name = "UserInfo"
		verbose_name_plural = "UserInfos"

	def getDict(self):
		return {'auth_id' : self.auth_id_id, 
				'name' : self.name, 'b_date' : str(self.b_date), 
				'place' : self.place, 'avatar' : utils.image_url_handler(self.avatar.name)}

# -----------
# Followers
# -----------

class Follow(models.Model):
	follower = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='follower')
	following = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='following')

	def __str__(self):
		return self.follower.login + " -> " + self.following.login

	class Meta:
		unique_together = (("follower", "following"),)

	def getDict(self):
		return {'id' : self.id, 'follower_id' : self.follower_id,
				'following_id' : self.following_id,}
		

# ----------------------
# User-Tobacco Object
# ----------------------

class UserTobacco(models.Model):
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
	tobacco = models.ForeignKey(Tobacco, on_delete=models.CASCADE)#, related_name='uto')
	strength_vote = models.SmallIntegerField(null=True, blank=True)
	smoke_vote = models.SmallIntegerField(null=True, blank=True)
	taste_vote = models.SmallIntegerField(null=True, blank=True)
	heat_vote = models.SmallIntegerField(null=True, blank=True)
	rating_vote = models.SmallIntegerField(null=True, blank=True)
	is_favorite = models.BooleanField(default=False)
	is_bookmark = models.BooleanField(default=False)

	def __str__(self):
		return self.user.login + " -> " + self.tobacco.brand + ' ' + self.tobacco.name

	class Meta:
		unique_together = (("user", "tobacco"),)
		verbose_name = "UserTobacco"
		verbose_name_plural = "UserTobaccos"

	def is_empty(self):
		return ((self.strength_vote is None) and (self.smoke_vote is None) and 
			(self.smoke_vote is None) and (self.taste_vote is None) and 
			(self.heat_vote is None) and (self.rating_vote is None) and 
			(self.is_favorite is False) and (self.is_bookmark is False))

	def getDict(self):
		return 	{ 
				'id': self.id, 'user_id': self.user_id, 'tobacco_id': self.tobacco_id,
				'strength_vote': self.strength_vote, 'smoke_vote': self.smoke_vote,
				'taste_vote': self.taste_vote, 'heat_vote': self.heat_vote,
				'rating_vote': self.rating_vote, 'is_favorite': self.is_favorite,
				'is_bookmark': self.is_bookmark,
				}

	def getEmptyDict(uid, tid):
		return 	{
				'user_id': uid, 'tobacco_id': tid,
				'strength_vote': None, 'smoke_vote': None,
				'taste_vote': None, 'heat_vote': None,
				'rating_vote': None, 'is_favorite': False,
				'is_bookmark': False,
				}

# ----------------------
# User-Mix Object
# ----------------------

class UserMix(models.Model):
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
	mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
	rating_vote = models.SmallIntegerField(null=True, blank=True)
	is_favorite = models.BooleanField(default=False)
	is_bookmark = models.BooleanField(default=False)

	def __str__(self):
		return self.user.login + " -> " + str(self.mix.id)

	class Meta:
		unique_together = (("user", "mix"),)
		verbose_name = "UserMix"
		verbose_name_plural = "UserMixes"

	def is_empty(self):
		return ((self.rating_vote is None) and 
			(self.is_favorite is False) and (self.is_bookmark is False))

	def getDict(self):
		return {'id' : self.id, 'user_id' : self.user_id, 
			'mix_id' : self.mix_id, 'rating_vote' : self.rating_vote, 
			'is_favorite' : self.is_favorite, 'is_bookmark' : self.is_bookmark}

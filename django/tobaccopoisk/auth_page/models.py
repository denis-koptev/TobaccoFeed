from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from datetime import datetime, timedelta
from auth_page import crypto
from django.utils import timezone
# Create your models here.

# ---------------
# Verifiend users
# ---------------

class User(models.Model):
	login = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=60)
	mail = models.CharField(max_length=256, unique=True)

	def __str__(self):
		return self.login

# --------
# Sessions
# --------

class Session(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=32, unique=True)
	expire = models.DateTimeField()

	def __str__(self):
		return self.id + ' ' + self.user.login

# set expire time
@receiver(pre_save, sender=Session)
def session_save(sender, instance, **kwargs):
	instance.expire = timezone.now() + timezone.timedelta(days=30)

# ----------------
# Unverified users
# ----------------

class Unuser(models.Model):
	login = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=60)
	mail = models.CharField(max_length=256, unique=True)
	token = models.CharField(max_length=32, unique=True)
	expire = models.DateTimeField()

	def __str__(self):
		return self.login

# password hashing and
# set expire time before saving
@receiver(pre_save, sender=Unuser)
def unuser_save(sender, instance, **kwargs):
	instance.expire = datetime.now() + timedelta(days=1)
from django.db import models
from django.conf import settings
from datetime import date
from tobaccopoisk import utils

# ------------------------
# Create storage to change url path
# 	and delete old file before uploading new one
# ------------------------

from django.core.files.storage import FileSystemStorage
import os
import re


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


path_and_rename = PathAndRename("tobacco_page/static/tobacco_page/tobaccos/")

# --------------
# End of routine
# --------------

EMPTY_TOBACCO = "tobacco_page/static/tobacco_page/tobaccos/empty_tobacco.png"


class Tobacco(models.Model):
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    release_date = models.DateField(null=True, blank=True, default=date.today)
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
        return self.brand.title() + ' ' + self.name.title()

    def getDict(self):
        return {
            'id': self.id, 'brand': self.brand, 'name': self.name,
            'release_date': str(self.release_date), 'description': self.description,
            'strength': self.strength, 'strength_votes': self.strength_votes,
            'smoke': self.smoke, 'smoke_votes': self.smoke_votes,
            'taste': self.taste, 'taste_votes': self.taste_votes,
            'heat': self.heat, 'heat_votes': self.heat_votes,
            'rating': self.rating, 'rating_votes': self.rating_votes,
            'image': utils.image_url_handler(str(self.image))
        }


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
#    for signal receivers
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
    tobaccos = models.ManyToManyField(Tobacco, related_name='mixes', through='MixTobacco')

    def __str__(self):
        return str(self.id) + ' : ' + " + ".join(to_view_str(t.brand) + ' ' + to_view_str(t.name) for t in self.tobaccos.all())

    class Meta:
        # The default ordering for the object,
        # 	for use when obtaining lists of objects:
        ordering = ('-pub_date',)

        # Custom multiple name
        verbose_name_plural = 'Mixes'


class MixTobacco(models.Model):
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    tobacco = models.ForeignKey(Tobacco, on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.mix.id) + ' -> ' + self.tobacco.brand + ' ' + self.tobacco.name

    class Meta:
        verbose_name = "MixTobacco"
        verbose_name_plural = "MixTobaccos"

# -------
# End of
# 	Mixes
# -------

# --------
# Start of
# 	Tags
# --------


class Tag(models.Model):
    tobacco = models.ManyToManyField('Tobacco', related_name='tags')
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return '#' + self.tag_name

# -------
# End of
# 	Tags
# -------

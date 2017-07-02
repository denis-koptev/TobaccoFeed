from django.contrib import admin

from .models import User, Follow

class FollowAdmin(admin.ModelAdmin):
	search_fields = ['follower__login', 'following__login', ]

admin.site.register(User)
admin.site.register(Follow, FollowAdmin)
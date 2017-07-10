from django.contrib import admin

from .models import User, Follow, UserTobacco, UserMix

class FollowAdmin(admin.ModelAdmin):
	search_fields = ['follower__login', 'following__login', ]

class UserTobaccoAdmin(admin.ModelAdmin):
	search_fields = ['user__login', 'tobacco__brand', 'tobacco__name',]

class UserMixAdmin(admin.ModelAdmin):
	search_fields = ['user__login',]

class UserAdmin(admin.ModelAdmin):
	search_fields = ['auth_id__login',]

admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(UserTobacco, UserTobaccoAdmin)
admin.site.register(UserMix, UserMixAdmin)
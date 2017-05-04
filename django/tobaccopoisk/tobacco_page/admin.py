from django.contrib import admin

# Register your models here.

from .models import Tobacco, Mix

class MixTobaccoInline(admin.StackedInline):
	model = Mix.tobaccos.through

class TobaccoAdmin(admin.ModelAdmin):
	inlines = [
		MixTobaccoInline,
	]

admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Mix)
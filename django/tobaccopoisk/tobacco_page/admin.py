from django.contrib import admin

# Register your models here.

from .models import Tobacco, Mix

class MixTobaccoInline(admin.StackedInline):
	model = Mix.tobaccos.through

class TobaccoAdmin(admin.ModelAdmin):
	inlines = [
		MixTobaccoInline,
	]

	search_fields = ['brand', 'name', ]

class MixAdmin(admin.ModelAdmin):
	search_fields = ['tobaccos__brand', 'tobaccos__name', ]

	# item options
	filter_horizontal = ("tobaccos",)

admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Mix, MixAdmin)

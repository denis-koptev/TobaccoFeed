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
	list_filter = ('release_date', 'brand', 'rating', )

class MixAdmin(admin.ModelAdmin):
	search_fields = ['tobaccos__brand', 'tobaccos__name', ]
	list_filter = ('pub_date', 'rating', )

	# item options
	filter_horizontal = ("tobaccos",)

admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Mix, MixAdmin)

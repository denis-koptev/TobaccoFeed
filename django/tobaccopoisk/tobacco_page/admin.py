from django.contrib import admin

# Register your models here.

from .models import Tobacco, Mix, Tag

class TobaccoMixInline(admin.StackedInline):
	model = Mix.tobaccos.through

class TobaccoTagInline(admin.StackedInline):
	model = Tag.tobacco.through

class TobaccoAdmin(admin.ModelAdmin):
	inlines = [
		TobaccoMixInline,
		TobaccoTagInline,
	]
	
	# for horizontal_filter of StackedInline
	# http://stackoverflow.com/questions/11657682/django-admin-interface-using-horizontal-filter-with-inline-manytomany-field

	search_fields = ['brand', 'name', ]
	list_filter = ('release_date', 'brand', 'rating', )

class MixAdmin(admin.ModelAdmin):
	search_fields = ['tobaccos__brand', 'tobaccos__name', ]
	list_filter = ('pub_date', 'rating', )

	# item options
	filter_horizontal = ("tobaccos",)

class TagAdmin(admin.ModelAdmin):
	search_fields = ['tag_name', ]

	# item options
	filter_horizontal = ("tobacco",)


admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Mix, MixAdmin)
admin.site.register(Tag, TagAdmin)

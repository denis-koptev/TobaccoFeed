from django.contrib import admin

# Register your models here.

from .models import Tobacco, Mix, Tag, MixTobacco
from .forms import TobaccoAdminForm, MixAdminForm

class TobaccoAdmin(admin.ModelAdmin):
	form = TobaccoAdminForm	
	search_fields = ['brand', 'name', ]
	list_filter = ('release_date', 'brand', 'rating', )

class MixTobaccoInline(admin.TabularInline):
    model = MixTobacco
    extra = 2 # how many rows to show

class MixAdmin(admin.ModelAdmin):
	inlines = (MixTobaccoInline,)
	search_fields = ['tobaccos__brand', 'tobaccos__name', ]
	list_filter = ('pub_date', 'rating', )

	# item options
	# filter_horizontal = ("tobaccos",)

class TagAdmin(admin.ModelAdmin):
	search_fields = ['tag_name', ]
	
	# item options
	filter_horizontal = ("tobacco",)


admin.site.register(Tobacco, TobaccoAdmin)
admin.site.register(Mix, MixAdmin)
admin.site.register(Tag, TagAdmin)

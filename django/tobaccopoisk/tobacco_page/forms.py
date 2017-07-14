from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Tobacco, Tag, Mix

# sponsored by
# http://stackoverflow.com/questions/11657682/django-admin-interface-using-horizontal-filter-with-inline-manytomany-field

class TobaccoAdminForm(forms.ModelForm):
	class Meta:
		model = Tobacco
		fields = 	[	
						'brand', 'name', 'description', 'release_date',
						'strength', 'strength_votes', 'smoke', 'smoke_votes',
						'taste', 'taste_votes', 'heat', 'heat_votes',
						'rating', 'rating_votes', 'image',
					]

	# define new form field
	# ModelMultipleChoiceField by default - a multiple select box
	tags = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		required=False,
		# use widget FilteredSelectMultiple
		# filter_horizontal uses it too
		widget=FilteredSelectMultiple(
			verbose_name='Tags',
			is_stacked=False
		)
	)

	mixes = forms.ModelMultipleChoiceField(
		queryset=Mix.objects.all(),
		required=False,
		# use widget FilteredSelectMultiple
		# filter_horizontal uses it too
		widget=FilteredSelectMultiple(
			verbose_name='Mixes',
			is_stacked=False
		)
	)

	# set the filtered queryset as the field's initial value
	def __init__(self, *args, **kwargs):
		super(TobaccoAdminForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.fields['tags'].initial = self.instance.tags.all()
			self.fields['mixes'].initial = self.instance.mixes.all()

	# we override the save method, 
	# so that we can set the related manager's contents 
	# to the same as what was in the form's POST data.
	def save(self, commit=True):
		tobacco = super(TobaccoAdminForm, self).save(commit=False)
		if commit:
			tobacco.save()

		if tobacco.pk:
			tobacco.tags = self.cleaned_data['tags']
			tobacco.mixes = self.cleaned_data['mixes']
			self.save_m2m()

		return tobacco

class MixAdminForm(forms.ModelForm):
	class Meta:
		model = Mix
		fields = 	[	
						'description', 'rating', 
						'rating_votes', 'tobaccos',
					]

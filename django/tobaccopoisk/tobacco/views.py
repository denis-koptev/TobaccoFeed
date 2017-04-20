from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Tobacco
from django.http import Http404

# Create your views here.

def tobacco_view(request, brand, name):
	tobacco = get_object_or_404(Tobacco, brand=brand, name=name)
	context = {'brand': brand.title(), 'name':name.title(),'description':tobacco.description,
			   'strength':tobacco.strength, 'taste':tobacco.taste, 'heat':tobacco.heat, 'smoke':tobacco.smoke,}
	return render(request, 'tobacco/index.html', context)
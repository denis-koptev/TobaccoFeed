from django.shortcuts import render
from django.http import HttpResponse
from .models import Tobacco

# Create your views here.

def tobacco_view(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		return render(request, 'error_404.html', {})

	context = {'brand': brand.title(), 'name':name.title(),'description':tobacco.description,
			   'strength':tobacco.strength, 'taste':tobacco.taste, 'heat':tobacco.heat, 'smoke':tobacco.smoke,}

	return render(request, 'tobacco/index.html', context)
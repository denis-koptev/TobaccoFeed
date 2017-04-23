from django.shortcuts import render
from django.http import HttpResponse
from .models import Tobacco

def image_url_handler(url):
	idx = url.find('/static/')
	return url[idx:]

def space_to_underscore(str):
	return str.replace(' ', '_')

def underscore_to_space(str):
	return str.replace('_', ' ')

def hyphen_to_underscore(str):
	return str.replace('-','_')

def underscore_to_hyphen(str):
	return str.replace('_','-')

def tobacco_view(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		return render(request, 'error_404.html', {})

	context = {'brand': underscore_to_space(brand.title()), 
	           'name': underscore_to_space(name.title()), 
	           'tobacco': tobacco, 
	           'image': image_url_handler(tobacco.image.name)}

	return render(request, 'tobacco/tobacco_page.html', context)
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

import json

def tobacco_search(request):
	
	def to_dict(inst):
		return 	{
				'brand': inst[0],
				'name': inst[1],
				'image': image_url_handler(inst[2]),
				}

	try:
		insts = Tobacco.objects.values_list('brand', 'name', 'image')
	except Tobacco.DoesNotExist:
		return HttpResponse("{}".format(json.dumps({"data": []}, ensure_ascii=False)))


	q = request.GET.get('q')
	data = [to_dict(inst) for inst in insts]

	return HttpResponse("{}".format(json.dumps({"data": data}, ensure_ascii=False)))
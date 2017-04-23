from django.http import HttpResponse
from tobacco.models import Tobacco
import json
# Create your views here.

def image_url_handler(url):
	idx = url.find('/static/')
	return url[idx:]

def underscore_to_space(str):
	return str.replace('_', ' ')

def tobacco(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		data = { 'result': 'false' }
	else:
		data = 	{	
				'result': 'true',
				'brand': underscore_to_space(brand.title()), 
				'name': underscore_to_space(name.title()),
				'description': tobacco.description,
				'strength': tobacco.strength, 
				'taste': tobacco.taste, 
				'heat': tobacco.heat, 
				'smoke': tobacco.smoke,
				'image': image_url_handler(tobacco.image.name),
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))
	
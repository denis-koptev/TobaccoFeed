from django.http import HttpResponse
from tobacco.models import Tobacco
import json
from search_page.engine import search as do_search
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
				'strength_votes': tobacco.strength_votes,
				'taste': tobacco.taste, 
				'taste_votes': tobacco.taste_votes,
				'heat': tobacco.heat, 
				'heat_votes': tobacco.heat_votes,
				'smoke': tobacco.smoke,
				'smoke_votes': tobacco.smoke_votes,
				'image': image_url_handler(tobacco.image.name),
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))

def search(request):

	q = request.GET.get('q')
	
	result = do_search(q)

	return HttpResponse("{}".format(json.dumps({'data': result}, ensure_ascii=False)))
	
import json
from django.http import HttpResponse
from tobacco_page.models import Tobacco
from search_page.engine import search as do_search
from tobaccopoisk import utils
# Create your views here.

def tobacco(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		data = { 'result': 'false' }
	else:
		data = 	{	
				'result': 			'true',
				'brand': 			utils.to_view_str(brand), 
				'name': 			utils.to_view_str(name),
				'description': 		tobacco.description,
				'strength': 		tobacco.strength, 
				'strength_votes': 	tobacco.strength_votes,
				'taste': 			tobacco.taste, 
				'taste_votes': 		tobacco.taste_votes,
				'heat': 			tobacco.heat, 
				'heat_votes': 		tobacco.heat_votes,
				'smoke': 			tobacco.smoke,
				'smoke_votes': 		tobacco.smoke_votes,
				'image': 			utils.image_url_handler(tobacco.image.name),
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))

def search(request):

	q = request.GET.get('q')
	
	result = do_search(q)

	return HttpResponse("{}".format(json.dumps({'data': result}, ensure_ascii=False)))
	
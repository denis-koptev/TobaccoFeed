from django.http import HttpResponse
from tobacco.models import Tobacco
# Create your views here.

def tobacco_view(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		data = { 'restult': 'false' }
	else:
		data = 
			{	
				'result': 'true',
				'brand': brand.title(), 
				'name':name.title(),
				'description':tobacco.description,
			   	'strength':tobacco.strength, 
			   	'taste':tobacco.taste, 
			   	'heat':tobacco.heat, 
			   	'smoke':tobacco.smoke,
			}

	return HttpResponse("{}".format(json.dumps(data)))
	
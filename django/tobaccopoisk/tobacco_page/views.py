from django.shortcuts import render
from .models import Tobacco
from tobaccopoisk import utils

def tobacco_view(request, brand, name):
	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		return render(request, 'error_404.html', {})

	context = {'brand': utils.to_view_str(brand), 
			   'name': utils.to_view_str(name), 
			   'tobacco': tobacco, 
			   'image': utils.image_url_handler(tobacco.image.name)}

	return render(request, 'tobacco_page/tobacco_page.html', context)

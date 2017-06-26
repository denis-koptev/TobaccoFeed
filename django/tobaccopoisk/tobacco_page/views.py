from django.shortcuts import render
from .models import Tobacco
from .models import Tag
from tobaccopoisk import utils
from auth_page import engine
from .models import Mix

def tobacco_view(request, brand, name):

	try:
		tobacco = Tobacco.objects.get(brand=brand, name=name)
	except Tobacco.DoesNotExist:
		return render(request, 'error_404.html', {})

	try:
		tags = Tag.objects.filter(tobacco=tobacco)
	except Tag.DoesNotExist:
		tags = []

	mixes = Mix.objects.filter(tobaccos=tobacco).order_by('-rating')

	if request.method == 'POST':
		return engine.unauthorize(request)

	login = engine.getAuthorized(request)


	context = {'brand': utils.to_view_str(brand), 
			   'name': utils.to_view_str(name), 
			   'tobacco': tobacco, 
			   'image': utils.image_url_handler(tobacco.image.name),
			   'tags': tags,
			   'login' : login,
			   'mixes' : mixes}

	return render(request, 'tobacco_page/tobacco_page.html', context)

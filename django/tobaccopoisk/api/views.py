import json
from django.http import HttpResponse
from tobacco_page.models import Tobacco
from search_page.engine import search as do_search
from tobaccopoisk import utils
from auth_page import engine
from auth_page.models import User
from user_page.models import UserTobacco
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

def get_usertobacco_by_names(request, username, brand, tobacco):

	tobacco = utils.to_db_str(tobacco)
	brand = utils.to_db_str(brand)

	usr = User.objects.filter(login=username)
	if len(usr) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'User not found'}, ensure_ascii=False)))

	tobac = Tobacco.objects.filter(brand=brand, name=tobacco)
	if len(tobac) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Tobacco not found'}, ensure_ascii=False)))

	uto = UserTobacco.objects.filter(user=usr, tobacco=tobac)
	if len(uto) == 0:
		data = 	{	
				'result': 			'true',
				'username': 		username, 
				'brand': 			brand,
				'tobacco': 			tobacco,

				'strength_vote': 	None,
				'taste_vote': 		None,
				'heat_vote': 		None,
				'smoke_vote': 		None,
				'rating_vote': 		None,
				'is_favorite': 		None,
				}
	else:
		data = 	{	
				'result': 			'true',
				'username': 		username, 
				'brand': 			brand,
				'tobacco': 			tobacco,

				'strength_vote': 	uto.strength_vote,
				'taste_vote': 		uto.taste_vote,
				'heat_vote': 		uto.heat_vote,
				'smoke_vote': 		uto.smoke_vote,
				'rating_vote': 		uto.rating_vote,
				'is_favorite': 		uto.is_favorite,
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))
	
def set_usertobacco_heat(request, token, brand, tobacco, vote):

	tobacco = utils.to_db_str(tobacco)
	brand = utils.to_db_str(brand)

	if vote not in range(1, 10):
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Vote should be positive integer not higher than 10'}, ensure_ascii=False)))

	user = engine.get_user_by_token(token)
	if user is None:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Session not found'}, ensure_ascii=False)))

	tobac = Tobacco.objects.filter(brand=brand, name=tobacco)
	if len(tobac) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Tobacco not found'}, ensure_ascii=False)))

	uto = UserTobacco.objects.filter(user=user, tobacco=tobac)
	if len(uto) == 0:
		uto = UserTobacco(user=user, tobacco=tobac, strength_vote=None, smoke_vote=None,
							taste_vote=None, heat_vote=None, rating_vote=None, is_favorite=None)

	uto.heat = vote
	uto.save()

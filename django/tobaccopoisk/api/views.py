import json
from django.http import HttpResponse
from search_page.engine import search as do_search
from tobaccopoisk import utils
from auth_page.models import User
from user_page.models import UserTobacco, UserMix
from tobacco_page.models import Tobacco, Mix
from user_page import api as user_api
# Create your views here.

def JSONResponse(data):
	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))

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

# ----------
# User API
# ----------

# UMO

def get_umo(request, username, mix_id):
	result = user_api.get_umo(username, mix_id)
	return JSONResponse(result)

def set_umo_rating(request, token, mix_id, vote):
	result = user_api.set_umo_int_param(token, mix_id, vote, 'rating')
	return JSONResponse(result)

def set_umo_favorite(request, token, mix_id, vote):
	result = user_api.set_umo_bool_param(token, mix_id, vote, 'favorite')
	return JSONResponse(result)

def set_umo_bookmark(request, token, mix_id, vote):
	result = user_api.set_umo_bool_param(token, mix_id, vote, 'bookmark')
	return JSONResponse(result)


# Follow

def userapi_follow(request, token, username):
	result = user_api.follow_user(token, username)
	return JSONResponse(result)

def userapi_is_follow(request, follower, following):
	result = user_api.is_follow(follower, following)
	return JSONResponse(result)

def userapi_unfollow(request, token, username):
	result = user_api.unfollow_user(token, username)
	return JSONResponse(result)


# UTO

def get_uto_by_names(request, username, brand, tobacco):
	result = user_api.get_uto_by_names(username, brand, tobacco)
	return JSONResponse(result)

def set_uto_heat(request, token, brand, tobacco, vote):
	result = user_api.set_uto_int_param(token, brand, tobacco, vote, 'heat')
	return JSONResponse(result)

def set_uto_strength(request, token, brand, tobacco, vote):
	result = user_api.set_uto_int_param(token, brand, tobacco, vote, 'strength')
	return JSONResponse(result)

def set_uto_taste(request, token, brand, tobacco, vote):
	result = user_api.set_uto_int_param(token, brand, tobacco, vote, 'taste')
	return JSONResponse(result)

def set_uto_smoke(request, token, brand, tobacco, vote):
	result = user_api.set_uto_int_param(token, brand, tobacco, vote, 'smoke')
	return JSONResponse(result)

def set_uto_rating(request, token, brand, tobacco, vote):
	result = user_api.set_uto_int_param(token, brand, tobacco, vote, 'rating')
	return JSONResponse(result)

def set_uto_favorite(request, token, brand, tobacco, vote):
	result = user_api.set_uto_bool_param(token, brand, tobacco, vote, 'favorite')
	return JSONResponse(result)

def set_uto_bookmark(request, token, brand, tobacco, vote):
	result = user_api.set_uto_bool_param(token, brand, tobacco, vote, 'bookmark')
	return JSONResponse(result)
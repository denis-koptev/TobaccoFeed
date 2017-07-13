import json
from django.http import HttpResponse
from search_page.engine import search as do_search
from tobaccopoisk import utils
from auth_page import engine
from auth_page.models import User
from user_page.models import UserTobacco, UserMix
from tobacco_page.models import Tobacco, Mix
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

# -------------------------
# UserTobacco Object (UTO)
# -------------------------

def get_usertobacco_by_names(request, username, brand, tobacco):

	tobacco = utils.to_db_str(tobacco)
	brand = utils.to_db_str(brand)

	usr = User.objects.filter(login=username)
	if len(usr) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'User not found'}, ensure_ascii=False)))
	usr = usr[0]

	tobac = Tobacco.objects.filter(brand=brand, name=tobacco)
	if len(tobac) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Tobacco not found'}, ensure_ascii=False)))
	tobac = tobac[0]

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
				'is_bookmark': 		None,
				}
	else:
		uto = uto[0]

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
				'is_bookmark': 		uto.is_bookmark,
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))
	
def set_uto_param(token, brand, tobacco, raw_vote, param):

	brand = utils.to_db_str(brand)
	tobacco = utils.to_db_str(tobacco)
	vote = raw_vote

	user = engine.get_user_by_token(token)
	if user is None:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Session not found'}, ensure_ascii=False)))

	tobac = Tobacco.objects.filter(brand=brand, name=tobacco)
	if len(tobac) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Tobacco not found'}, ensure_ascii=False)))
	tobac = tobac[0]

	uto = UserTobacco.objects.filter(user=user, tobacco=tobac)
	if len(uto) == 0:
		uto = UserTobacco(user=user, tobacco=tobac, strength_vote=None, smoke_vote=None,
							taste_vote=None, heat_vote=None, rating_vote=None, 
							is_favorite=False, is_bookmark=False)
	else:
		uto = uto[0]

	if param == 'rating':
		uto.rating_vote = vote
	elif param == 'taste':
		uto.taste_vote = vote
	elif param == 'smoke':
		uto.smoke_vote = vote
	elif param == 'strength':
		uto.strength_vote = vote
	elif param == 'heat':
		uto.heat_vote = vote
	elif param == 'favorite':
		uto.is_favorite = vote
	elif param == 'bookmark':
		uto.is_bookmark = vote


	# Save and delete objects
	try:
		if uto.is_empty() is True:
			uto.delete()
		else:
			uto.save()
	except:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Update error'}, ensure_ascii=False)))
	else:
		return HttpResponse("{}".format(json.dumps({'result': True, 'desc': 'Heat vote updated'}, ensure_ascii=False)))

def set_uto_vote_param(token, brand, tobacco, vote, param):

	vote = int(vote)
	if vote not in range(0, 11):
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Vote should be positive integer not higher than 10 or 0 (None)'}, ensure_ascii=False)))
	if vote == 0:
		vote = None

	return set_uto_param(token, brand, tobacco, vote, param)

def set_usertobacco_heat(request, token, brand, tobacco, vote):
	return set_uto_vote_param(token, brand, tobacco, vote, 'heat')

def set_usertobacco_strength(request, token, brand, tobacco, vote):
	return set_uto_vote_param(token, brand, tobacco, vote, 'strength')

def set_usertobacco_taste(request, token, brand, tobacco, vote):
	return set_uto_vote_param(token, brand, tobacco, vote, 'taste')

def set_usertobacco_smoke(request, token, brand, tobacco, vote):
	return set_uto_vote_param(token, brand, tobacco, vote, 'smoke')

def set_usertobacco_rating(request, token, brand, tobacco, vote):
	return set_uto_vote_param(token, brand, tobacco, vote, 'rating')

def set_uto_bool_param(token, brand, tobacco, vote, param):

	if vote == '1':
		vote = True
	elif vote == '0':
		vote == False
	else:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Vote should be 0 (False) or 1 (True)'}, ensure_ascii=False)))

	return set_uto_param(token, brand, tobacco, vote, param)

def set_usertobacco_favorite(request, token, brand, tobacco, vote):
	return set_uto_bool_param(token, brand, tobacco, vote, 'favorite')

def set_usertobacco_bookmark(request, token, brand, tobacco, vote):
	return set_uto_bool_param(token, brand, tobacco, vote, 'bookmark')

# ----------------------
# UserMix Object (UMO)
# ----------------------

def get_usermix(request, username, mix_id):

	usr = User.objects.filter(login=username)
	if len(usr) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'User not found'}, ensure_ascii=False)))
	usr = usr[0]

	mix = Mix.objects.filter(pk=mix_id)
	if len(mix) == 0:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Mix with specified id not found'}, ensure_ascii=False)))
	mix = mix[0]

	umo = UserMix.objects.filter(user=usr, mix=mix)
	if len(umo) == 0:
		data = 	{	
				'result': 			'true',
				'username': 		username, 
				'mix_id': 			mix_id,

				'rating_vote': 		None,
				'is_favorite': 		None,
				'is_bookmark': 		None,
				}
	else:
		umo = umo[0]

		data = 	{	
				'result': 			'true',
				'username': 		username, 
				'mix_id': 			mix_id,

				'rating_vote': 		umo.rating_vote,
				'is_favorite': 		umo.is_favorite,
				'is_bookmark': 		umo.is_bookmark,
				}

	return HttpResponse("{}".format(json.dumps(data, ensure_ascii=False)))

def set_umo_param(token, mix_id, raw_vote, param):

	vote = raw_vote

	user = engine.get_user_by_token(token)
	if user is None:
		return 'Session not found'

	mix = Mix.objects.filter(pk=mix_id)
	if len(mix) == 0:
		return 'Mix not found'
	mix = mix[0]

	umo = UserMix.objects.filter(user=user, mix=mix)
	if len(umo) == 0:
		umo = UserMix(user=user, mix=mix, rating_vote=None, is_favorite=False, is_bookmark=False)
	else:
		umo = umo[0]

	if param == 'rating':
		umo.rating_vote = vote
	elif param == 'favorite':
		umo.is_favorite = vote
	elif param == 'bookmark':
		umo.is_bookmark = vote

	try:
		if umo.is_empty():
			umo.delete()
		else:
			umo.save()

	except:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Update error'}, ensure_ascii=False)))
	else:
		return HttpResponse("{}".format(json.dumps({'result': True, 'desc': 'Rating vote updated'}, ensure_ascii=False)))

def set_umo_vote_param(token, mix_id, vote, param):

	vote = int(vote)
	if vote not in range(1, 11):
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Vote should be positive integer not higher than 10'}, ensure_ascii=False)))

	return set_umo_param(token, mix_id, vote, param)

def set_umo_bool_param(token, mix_id, vote, param):
	
	if vote == '1':
		vote = True
	elif vote == '0':
		vote == False
	else:
		return HttpResponse("{}".format(json.dumps({'result': False, 'desc': 'Vote should be 0 (False) or 1 (True)'}, ensure_ascii=False)))

	return set_umo_param(token, mix_id, vote, param)

def set_usermix_rating(request, token, mix_id, vote):
	return set_umo_vote_param(token, mix_id, vote, 'rating')

def set_usermix_favorite(request, token, mix_id, vote):
	return set_umo_bool_param(token, mix_id, vote, 'favorite')

def set_usermix_bookmark(request, token, mix_id, vote):
	return set_umo_bool_param(token, mix_id, vote, 'bookmark')
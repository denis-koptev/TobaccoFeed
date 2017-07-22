from auth_page.models import User as AuthUser, Session
from auth_page.engine import get_user_by_token
from tobacco_page.models import Tobacco, Mix
from user_page.models import Follow, User, UserTobacco, UserMix
from django.db import IntegrityError, DatabaseError
from tobaccopoisk import utils

# --------------
# Follow 
# --------------

def follow_user(token, username):

	# get follower by token

	follower = get_user_by_token(token)
	if follower is None:
		return {'result': False, 'desc': 'Session not found'}

	# find and get following user

	try:
		following = AuthUser.objects.get(login=username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'User with specified username not found'}	

	try:
		new_follow = Follow(follower=follower, following=following)
		new_follow.save()
	except IntegrityError:
		return {'result': False, 'desc': 'Following relation already exists'}
	except DatabaseError:
		return {'result': False, 'desc': 'Can not create following relation'}

	return {'result': True, 'desc': 'Following relation created'}


def is_follow(follower_username, following_username):

	try:
		Follow.objects.get(follower__login=follower_username, following__login=following_username)
	except Follow.DoesNotExist:
		return {'result': False, 'desc': 'Following relation was not found'}

	return {'result': True, 'desc': 'Following relation exists'}


def unfollow_user(token, username):

	# get follower by token

	follower = get_user_by_token(token)
	if follower is None:
		return {'result': False, 'desc': 'Session not found'}

	try:
		follow = Follow.objects.get(follower=follower, following__login=username)
	except Follow.DoesNotExist:
		return {'result': False, 'desc': 'Following relation with specified user does not exist'}

	try:
		follow.delete()
	except DatabaseError:
		return {'result': False, 'desc': 'Can not remove following relation'}

	return {'result': True, 'desc': 'Following relation removed'}


# ------
# UTO
# ------

def get_uto_by_names(username, brand, tobacco):

	tobacco = utils.to_db_str(tobacco)
	brand = utils.to_db_str(brand)

	# get user

	try:
		usr = AuthUser.objects.get(login=username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'User not found'}

	# get tobacco

	try:
		tobac = Tobacco.objects.get(brand=brand, name=tobacco)
	except Tobacco.DoesNotExist:
		return {'result': False, 'desc': 'Tobacco not found'}

	# get UTO

	try:

		uto = UserTobacco.objects.get(user=usr, tobacco=tobac)

	except UserTobacco.DoesNotExist:

		data = 	{	
				'result': 			True,
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

		data = 	{	
				'result': 			True,
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

	return data


def set_uto_param(token, brand, tobacco, raw_vote, param):

	brand = utils.to_db_str(brand)
	tobacco = utils.to_db_str(tobacco)
	vote = raw_vote

	user = get_user_by_token(token)
	if user is None:
		return {'result': False, 'desc': 'Session not found'}

	# get tobacco

	try:
		tobac = Tobacco.objects.get(brand=brand, name=tobacco)
	except Tobacco.DoesNotExist:
		return {'result': False, 'desc': 'Tobacco not found'}

	try:
		uto = UserTobacco.objects.get(user=user, tobacco=tobac)
	except UserTobacco.DoesNotExist:
		uto = UserTobacco(	user=user, tobacco=tobac, 
							strength_vote=None, smoke_vote=None,
							taste_vote=None, heat_vote=None, rating_vote=None, 
							is_favorite=False, is_bookmark=False)

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


	# Save or delete objects

	try:

		if uto.is_empty() is True:
			uto.delete()
		else:
			uto.save()

	except DatabaseError:
		return {'result': False, 'desc': 'Update error'}

	return {'result': True, 'desc': 'Heat vote updated'}


def set_uto_int_param(token, brand, tobacco, vote, param):

	vote = int(vote)

	if vote not in range(0, 11):
		return {'result': False, 'desc': 'Vote should be positive integer not higher than 10 or 0 (None)'}

	if vote == 0:
		vote = None

	return set_uto_param(token, brand, tobacco, vote, param)


def set_uto_bool_param(token, brand, tobacco, vote, param):

	if vote == '1':
		vote = True
	elif vote == '0':
		vote == False
	else:
		return {'result': False, 'desc': 'Vote should be 0 (False) or 1 (True)'}

	return set_uto_param(token, brand, tobacco, vote, param)


# ------
# UMO
# ------

def get_umo(username, mix_id):

	# get user

	try:
		usr = AuthUser.objects.get(login=username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'User not found'}

	# get mix by id

	try:
		mix = Mix.objects.get(id=mix_id)
	except Mix.DoesNotExist:
		return {'result': False, 'desc': 'Mix with specified id not found'}

	# get umo

	try:

		umo = UserMix.objects.get(user=usr, mix=mix)

	except UserMix.DoesNotExist:

		data = 	{	
				'result': 			True,
				'username': 		username, 
				'mix_id': 			mix_id,

				'rating_vote': 		None,
				'is_favorite': 		None,
				'is_bookmark': 		None,
				}

	else:

		data = 	{	
				'result': 			True,
				'username': 		username, 
				'mix_id': 			mix_id,

				'rating_vote': 		umo.rating_vote,
				'is_favorite': 		umo.is_favorite,
				'is_bookmark': 		umo.is_bookmark,
				}

	return data


def set_umo_param(token, mix_id, raw_vote, param):

	vote = raw_vote

	user = get_user_by_token(token)
	if user is None:
		return {'result': False, 'desc': 'Session not found'}

	# get mix by id
	try:
		mix = Mix.objects.get(pk=mix_id)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'Mix with specified id not found'}

	# get umo
	try:
		umo = UserMix.objects.get(user=user, mix=mix)
	except UserMix.DoesNotExist:
		umo = UserMix(user=user, mix=mix, rating_vote=None, is_favorite=False, is_bookmark=False)

	# set vote
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

	except DatabaseError:
		return {'result': False, 'desc': 'Update error'}
	
	return {'result': True, 'desc': 'Rating vote updated'}


def set_umo_int_param(token, mix_id, vote, param):

	vote = int(vote)
	if vote not in range(1, 11):
		return {'result': False, 'desc': 'Vote should be positive integer not higher than 10'}

	return set_umo_param(token, mix_id, vote, param)


def set_umo_bool_param(token, mix_id, vote, param):
	
	if vote == '1':
		vote = True
	elif vote == '0':
		vote == False
	else:
		return {'result': False, 'desc': 'Vote should be 0 (False) or 1 (True)'}

	return set_umo_param(token, mix_id, vote, param)

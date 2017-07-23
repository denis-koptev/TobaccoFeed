import json
from django.http import HttpResponse

from django.db import connection
from tobaccopoisk import utils, settings
from django.db.models import Prefetch

from auth_page.models import User as AuthUser
from user_page.models import User, Follow

def JSONResponse(data, status=200):
	if settings.DEBUG is True:
		data['db_queries'] = len(connection.queries)

	json_data = "{}".format(json.dumps(data, ensure_ascii=False))
	return HttpResponse(json_data, status=status)

def getIntParam(request, param, default):
	p = request.GET.get(param)
	if (p is not None) and (p.isdigit()):
		return int(p)
	else:
		return default

def getUserDict(user):
	user_dict = {}

	user_dict['id'] = user.id
	user_dict['username'] = user.login
	user_dict['email'] = user.mail
	user_dict['info'] = {
						'name' : user.info.name,
						'birthdate' : str(user.info.b_date),
						'place' : user.info.place,
						'avatar' : utils.image_url_handler(str(user.info.avatar)),
						}

	return user_dict

def getFollowingDict(user):
	following_array = []

	for flwers in user.follower.select_related('following__info').all():
		following_array.append(getUserDict(flwers.following))

	return {'count' : len(following_array), 'users' : following_array}

def getFollowersDict(user):
	followers_array = []

	for flwing in user.following.select_related('follower__info').all():
		followers_array.append(getUserDict(flwing.follower))

	return {'count' : len(followers_array), 'users' : followers_array}

def users(request):
	"""
	Params:
		[int] offset
		[int] limit
	"""
	offset = getIntParam(request, 'offset', None)
	limit = getIntParam(request, 'limit', None)

	users = AuthUser.objects.select_related('info').all()[offset:offset+limit]

	users_array = []
	for user in users:
		users_array.append(getUserDict(user))

	data = 	{
			'users' : users_array, 
			'count' : len(users_array), 
			'total' : AuthUser.objects.count(),
			}
	
	return JSONResponse({'status' : 200, 'data' : data})

def user(request, username):
	try:
		user = AuthUser.objects
		user = user.select_related('info')
		user = user.prefetch_related('follower')
		user = user.prefetch_related('following')
		user = user.get(login=username)

		user_dict = getUserDict(user)
		user_dict['following'] = getFollowingDict(user)
		user_dict['followers'] = getFollowersDict(user)

		data = {
			'user' : user_dict,
			}

		return JSONResponse({'status' : 200, 'data' : data})

	except AuthUser.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'User with specified name not found'})

import json
from django.http import HttpResponse

from django.db import DatabaseError
from django.db import connection
from tobaccopoisk import utils, settings

from auth_page.models import User as AuthUser
from user_page.models import User, Follow, UserTobacco
from tobacco_page.models import Tobacco

def JSONResponse(data):
	if settings.DEBUG is True:
		data['db_queries'] = len(connection.queries)

	json_data = "{}".format(json.dumps(data, ensure_ascii=False))
	return HttpResponse(json_data, status=data['status'])

def getIntParam(request, param, default):
	p = request.GET.get(param)
	if (p is not None) and (p.isdigit()):
		return int(p)
	else:
		return default

def getVoteParam(request, param, default):
	p = request.GET.get(param)

	if p is None:
		return default

	if p == 'none':
		return None

	if p.isdigit():
		p = int(p)
		if 1 <= p and p <= 10:
			return p
		else:
			return default

def getBoolParam(request, param, default):
	p = request.GET.get(param)

	if p == 'true':
		return True

	if p == 'false':
		return False

	return default

def getParam(request, param, default):
	p = request.GET.get(param)
	if p is not None:
		return p
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
		[int] offset (default : 0)
		[int] limit (default : 10)
	Examples:
		/api/v2/users
		/api/v2/users?offset=5&limit=2
	"""
	offset = getIntParam(request, 'offset', 0)
	limit = getIntParam(request, 'limit', 10)
	limit += offset

	users = AuthUser.objects.select_related('info').all()[offset:limit]

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
	"""
	Params:
	Examples:
		/api/v2/users/<username>
	"""
	try:
		user = AuthUser.objects
		user = user.select_related('info')
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

def tobaccos(request):
	"""
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
		[str] brand
		[str] name
	Examples:
		/api/v2/tobaccos
		/api/v2/tobaccos?offset=5&limit=2
	"""

	brand = getParam(request, 'brand', None)
	name = getParam(request, 'name', None)
	offset = getIntParam(request, 'offset', 0)
	limit = getIntParam(request, 'limit', 10)
	limit += offset

	tobaccos = Tobacco.objects
	if brand is not None:
		tobaccos = tobaccos.filter(brand=brand)
	if name is not None:
		tobaccos = tobaccos.filter(name=name)

	ts = tobaccos.all()[offset:limit]

	tobaccos_array = []
	for t in ts:
		tobaccos_array.append(t.getDict())

	data = 	{
			'tobaccos' : tobaccos_array, 
			'count' : len(tobaccos_array), 
			'total' : tobaccos.count(),
			}
	
	return JSONResponse({'status' : 200, 'data' : data})

def tobacco(request, **kwargs):
	"""
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
	Examples:
		/api/v2/tobaccos/<brand>/<name>
		/api/v2/tobaccos/<tid>
	"""
	tid = kwargs.get('tid')
	brand = kwargs.get('brand')
	name = kwargs.get('name')

	try:
		if tid is not None:
			tobacco = Tobacco.objects.get(pk=tid) 
		else:
			tobacco = Tobacco.objects.get(brand=brand, name=name)

		data = {
			'tobacco' : tobacco.getDict(),
			}

		return JSONResponse({'status' : 200, 'data' : data})

	except Tobacco.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'Tobacco not found'})

def utos(request, username):
	"""
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
	Examples:
		/api/v2/users/<username>/tobaccos
	"""

	print(request.get_full_path())

	offset = getIntParam(request, 'offset', 0)
	limit = getIntParam(request, 'limit', 10)
	limit += offset

	_utos = UserTobacco.objects.filter(user__login=username)
	utos = _utos.all()[offset:limit]

	utos_array = []
	for uto in utos:
		utos_array.append(uto.getDict())

	data = 	{
			'utos' : utos_array,
			'count' : len(utos_array), 
			'total' : _utos.count(),
			}
	
	return JSONResponse({'status' : 200, 'data' : data})

def uto_get(request, username, **kwargs):
	"""
	Params:
		[POST/GET] method
	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>
		/api/v2/users/<username>/tobaccos/<tid>
	"""
	method = getParam(request, 'method', 0)
	if method == 'post':
		return uto_post(request, username, **kwargs)

	tid = kwargs.get('tid')
	brand = kwargs.get('brand')
	name = kwargs.get('name')

	try:
		_uto = UserTobacco.objects.filter(user__login=username)

		if tid is not None:
			uto = _uto.get(tobacco__id=tid) 
		else:
			uto = _uto.get(tobacco__brand=brand, tobacco__name=name)

		data = {
			'uto' : uto.getDict(),
			}

		return JSONResponse({'status' : 200, 'data' : data})

	except UserTobacco.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'UTO not found'})

def uto_post(request, username, **kwargs):
	"""
	Params:
		[1...10/none] strength_vote
		[1...10/none] smoke_vote
		[1...10/none] heat_vote
		[1...10/none] taste_vote
		[1...10/none] rating_vote
		[true/false] is_favorite
		[true/false] is_bookmark

	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>
		/api/v2/users/<username>/tobaccos/<tid>
	"""
	
	tid = kwargs.get('tid')
	brand = kwargs.get('brand')
	name = kwargs.get('name')

	# get uto from db
	try:
		_uto = UserTobacco.objects.filter(user__login=username)

		if tid is not None:
			uto = _uto.get(tobacco__id=tid) 
		else:
			uto = _uto.get(tobacco__brand=brand, tobacco__name=name)


	except UserTobacco.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'UTO not found'})

	# get params

	strength_vote = getVoteParam(request, 'strength_vote', 0)
	smoke_vote = getVoteParam(request, 'smoke_vote', 0)
	heat_vote = getVoteParam(request, 'heat_vote', 0)
	taste_vote = getVoteParam(request, 'taste_vote', 0)
	rating_vote = getVoteParam(request, 'rating_vote', 0)
	is_favorite = getBoolParam(request, 'is_favorite', None)
	is_bookmark = getBoolParam(request, 'is_bookmark', None)

	# update params

	if strength_vote != 0:
		uto.strength_vote = strength_vote

	if smoke_vote != 0:
		uto.smoke_vote = smoke_vote
		
	if heat_vote != 0:
		uto.heat_vote = heat_vote
		
	if taste_vote != 0:
		uto.taste_vote = taste_vote
		
	if rating_vote != 0:
		uto.rating_vote = rating_vote

	if is_favorite is not None:
		uto.is_favorite = is_favorite

	if is_bookmark is not None:
		uto.is_bookmark = is_bookmark

	# save

	try:
		uto.save()
		return JSONResponse({'status' : 200})
	except DatabaseError:
		return JSONResponse({'status' : 400, 'message' : 'Data update error'})

def uto(request, username, **kwargs):

	if request.method == 'GET':
		return uto_get(request, username, **kwargs)
	elif request.method == 'POST':
		return uto_post(request, username, **kwargs)
	else:
		return JSONResponse({'status' : 400, 'message' : 'Unknown request method'})

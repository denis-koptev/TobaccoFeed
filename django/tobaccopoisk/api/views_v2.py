import json
from django.http import HttpResponse

from django.db import DatabaseError, IntegrityError
from django.db import connection
from tobaccopoisk import utils, settings
from auth_page import engine as auth_engine

from auth_page.models import User as AuthUser
from user_page.models import User, Follow, UserTobacco
from tobacco_page.models import Tobacco

def JSONResponse(data):
	if settings.DEBUG is True:
		data['db_queries'] = len(connection.queries)

	status = data.get('status', 200)

	json_data = "{}".format(json.dumps(data, ensure_ascii=False))
	return HttpResponse(json_data, status=status)

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
	Descriptions:
		Get list users from all users pool
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
	Description:
		Get info about specified user
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
	Description:
		Get list of tobaccos from all tobaccos pool
		Able to filter by brand and name
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
	Description:
		Get info about specified tobacco
	Params:
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

def spec_utos(request, username):
	"""
	Description:
		Get all UTOs of specified user
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
	Examples:
		/api/v2/users/<username>/tobaccos
	"""

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

def uto_get_explicit(request, username, **kwargs):
	"""
	Description:
		Get UTO info about specified tobacco
	Params:
		[POST/GET] method
		[true/false] explicit
	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>?explicit=true
		/api/v2/users/<username>/tobaccos/<tid>?explicit=true
	"""

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

def uto_get(request, username, **kwargs):
	"""
	Description:
		Get UTO info about specified tobacco
	Params:
		[true/false] explicit
	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>
		/api/v2/users/<username>/tobaccos/<tid>
	"""

	explicit = getBoolParam(request, 'explicit', False)
	if explicit == True:
		return uto_get_explicit(request, username, **kwargs)

	tid = kwargs.get('tid')
	brand = kwargs.get('brand')
	name = kwargs.get('name')

	try:
		_tobacco = Tobacco.objects

		if tid is not None:
			tobacco = _tobacco.get(pk=tid) 
		else:
			tobacco = _tobacco.get(brand=brand, name=name)

	except Tobacco.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'Specified tobacco not found'})

	try:
		user = AuthUser.objects.get(login=username)
	except AuthUser.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'Specified user not found'})

	try:
		uto = UserTobacco.objects.get(user=user, tobacco=tobacco)

		data = { 'uto' : uto.getDict() }

		return JSONResponse({'status' : 200, 'data' : data})

	except UserTobacco.DoesNotExist:
		return JSONResponse({'status' : 200, 'data' : UserTobacco.getEmptyDict(user.id, tobacco.id)})

def uto_post(request, username, **kwargs):
	"""
	Description:
		Update UTO for specified tobacco
	Params:
		[1...10/none] strength_vote
		[1...10/none] smoke_vote
		[1...10/none] heat_vote
		[1...10/none] taste_vote
		[1...10/none] rating_vote
		[true/false] is_favorite
		[true/false] is_bookmark

	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>?<param>=<value>
		/api/v2/users/<username>/tobaccos/<tid>?<param>=<value>
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
	"""
	Description:
		Read and Write UTO methods
	Params:
		[post/get] method
	Examples:
		/api/v2/users/<username>/tobaccos/<brand>/<name>
		/api/v2/users/<username>/tobaccos/<tid>?method=get
	"""

	method = getParam(request, 'method', None)
	if method is None:
		if request.method == 'GET':
			return uto_get(request, username, **kwargs)
		elif request.method == 'POST':
			return uto_post(request, username, **kwargs)

	elif method == 'post':
		return uto_post(request, username, **kwargs)
	elif method == 'get':
		return uto_get(request, username, **kwargs)

	return JSONResponse({'status' : 400, 'message' : 'Request method not supported for this call'})

def utos(request):
	"""
	Description:
		Get all UTOs in pool
		Or filter by some params
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
		[str] username
		[str] brand
		[str] tobacconame
		[int] tid			- tobacco id
	Examples:
		/api/v2/uto
		/api/v2/uto?username=<username>&brand=<brand>
	"""

	tid = getIntParam(request, 'tid', None)
	brand = getParam(request, 'brand', None)
	tobacconame = getParam(request, 'tobacconame', None)
	username = getParam(request, 'username', None)

	offset = getIntParam(request, 'offset', 0)
	limit = getIntParam(request, 'limit', 10)
	limit += offset

	_utos = UserTobacco.objects

	if username is not None:
		_utos = _utos.filter(user__login=username)
	if brand is not None:
		_utos = _utos.filter(tobacco__brand=brand)
	if tobacconame is not None:
		_utos = _utos.filter(tobacco__name=tobacconame)
	if tid is not None:
		_utos = _utos.filter(tobacco_id=tid)

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

def ufos_get(request):
	"""
	Description:
		Get UFOs in pool
		Or foltered by param
	Params:
		[int] offset (default : 0)
		[int] limit (default : 10)
		[str] follower_name
		[str] following_name
		[str] follower_id
		[str] following_id
	Examples:
		[GET] /api/v2/ufos
		[GET] /api/v2/ufos?follower_name=<japroc>
		[GET] /api/v2/ufos?follower_name=<japroc>&following_id=1
	"""

	follower_name = getParam(request, 'follower_name', None)
	following_name = getParam(request, 'following_name', None)
	follower_id = getIntParam(request, 'follower_id', None)
	following_id = getIntParam(request, 'following_id', None)

	offset = getIntParam(request, 'offset', 0)
	limit = getIntParam(request, 'limit', 10)
	limit += offset

	_ufos = Follow.objects

	if follower_name is not None:
		_ufos = _ufos.filter(follower__login=follower_name)
	if following_name is not None:
		_ufos = _ufos.filter(following__login=following_name)
	if follower_id is not None:
		_ufos = _ufos.filter(follower_id=follower_id)
	if following_id is not None:
		_ufos = _ufos.filter(following_id=following_id)

	ufos = _ufos.all()[offset:limit]

	ufos_array = []
	for ufo in ufos:
		ufos_array.append(ufo.getDict())

	data = 	{
			'utos' : ufos_array,
			'count' : len(ufos_array), 
			'total' : _ufos.count(),
			}
	
	return JSONResponse({'status' : 200, 'data' : data})

def ufos_post(request):
	"""
	Description:
		Follow specified user by name or param
		using token
	Params:
		[str] token
		[str] username
		[int] userid
	Examples:
		[POST] /api/v2/ufo?token=<str>&username=<str>
		[POST] /api/v2/ufo?token=<str>&userid=<int>
	"""

	# get params
	token = getParam(request, 'token', None)
	username = getParam(request, 'username', None)
	userid = getIntParam(request, 'userid', None)

	# check params
	if token is None:
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})
	if (username is None) and (userid is None):
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})
	if (username is not None) and (userid is not None):
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})

	# get follower by token
	follower = auth_engine.get_user_by_token(token)
	if follower is None:
		return JSONResponse({'status' : 400, 'message' : 'Incorrect token'})

	# get following by id or name
	try:
		_following = AuthUser.objects
		if username is not None:
			following = _following.get(login=username)
		else:
			following = _following.get(pk=userid)
	except AuthUser.DoesNotExist:
		return JSONResponse({'status' : 400, 'message' : 'Specified user not found'})

	# save and return response
	try:
		ufo = Follow(follower=follower, following=following)
		ufo.save()
		return JSONResponse({'status' : 200, 'message' : 'Follow relation created'})
	except IntegrityError:
		return JSONResponse({'status' : 200, 'message' : 'Follow relation already exist'})
	except DatabaseError:
		return JSONResponse({'status' : 500, 'message' : 'Create follow error'})
	else:
		return JSONResponse({'status' : 500, 'message' : 'Unknown internal error'})

def ufos_delete(request):
	"""
	Description:
		Delete follow relation from user specifiedd by token
		to user specified by name or id
	Params:
		[str] token
		[str] username
		[int] userid
	Examples:
		[POST]   /api/v2/ufo?token=<str>&username=<str>&method=<delete>
		[DELETE] /api/v2/ufo?token=<str>&userid=<int>
	"""

	# get params
	token = getParam(request, 'token', None)
	username = getParam(request, 'username', None)
	userid = getIntParam(request, 'userid', None)

	# check params
	if token is None:
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})
	if (username is None) and (userid is None):
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})
	if (username is not None) and (userid is not None):
		return JSONResponse({'status' : 400, 'message' : 'Incorrect request'})

	# get follower by token
	follower = auth_engine.get_user_by_token(token)
	if follower is None:
		return JSONResponse({'status' : 400, 'message' : 'Incorrect token'})

	# get and delete follow relation
	try:
		_follow = Follow.objects.filter(follower=follower)
		if username is not None:
			follow = _follow.filter(following__login=username).delete()
		else:
			follow = _follow.filter(following__pk=userid).delete()

		return JSONResponse({'status' : 200})
	except DatabaseError:
		return JSONResponse({'status' : 500, 'message' : 'Unknown internal error'})

def ufos(request):
	"""
	Description:
		Read and Write UFO methods
	Params:
		[get] method
	Examples:
		/api/v2/ufo?method=get
		/api/v2/ufo?method=post
	"""

	method = getParam(request, 'method', None)
	if method is None:
		if request.method == 'GET':
			return ufos_get(request)
		if request.method == 'POST':
			return ufos_post(request)
		if request.method == 'DELETE':
			return ufos_delete(request)

	elif method == 'get':
		return ufos_get(request)
	elif method == 'post':
		return ufos_post(request)
	elif method == 'delete':
		return ufos_delete(request)

	return JSONResponse({'status' : 400, 'message' : 'Request method not supported for this call'})


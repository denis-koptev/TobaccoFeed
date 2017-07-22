from auth_page.models import User as AuthUser, Session
from auth_page.engine import get_user_by_token
from .models import Follow
from django.db import IntegrityError, DatabaseError

def follow_user(token, username):
	# get follower by token
	follower = get_user_by_token(token)
	if follower == None:
		return {'result': False, 'desc': 'Token was not recognized'}

	# find and get following user
	followings = AuthUser.objects.filter(login=username)
	if len(followings) == 0:
		return {'result': False, 'desc': 'User with specified username not found'}
	following = followings[0]	

	try:
		new_follow = Follow(follower=follower, following=following)
		new_follow.save()
	except IntegrityError:
		return {'result': False, 'desc': 'Follow already exists'}
	except DatabaseError:
		return {'result': False, 'desc': 'Cant create follow'}
	else:
		return {'result': True, 'desc': 'Follow created'}


def is_follow(follower_username, following_username):
	# find and get follower user
	try:
		follower = AuthUser.objects.get(login=follower_username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'Follower user with specified username not found'}


	# find and get following user
	try:
		following = AuthUser.objects.get(login=following_username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'Following user with specified username not found'}

	# get Follow object
	try:
		Follow.objects.get(follower=follower, following=following)
	except Follow.DoesNotExist:
		return {'result': False, 'desc': 'Follow does not exist'}
	else:
		return {'result': True, 'desc': 'Follow exists'}


def unfollow_user(token, username):
	# get follower by token
	follower = get_user_by_token(token)
	if follower == None:
		return {'result': False, 'desc': 'Token was not recognized'}

	# find and get following user
	try:
		following = AuthUser.objects.get(login=username)
	except AuthUser.DoesNotExist:
		return {'result': False, 'desc': 'User with specified username not found'}	

	try:
		follow = Follow.objects.get(follower=follower, following=following)
	except Follow.DoesNotExist:
		return {'result': False, 'desc': 'Follow to specified user does not exist'}

	try:
		follow.delete()
	except DatabaseError:
		return {'result': False, 'desc': 'Cant remove follow'}

	return {'result': True, 'desc': 'Follow removed'}

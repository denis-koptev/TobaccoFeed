from django.shortcuts import render
from auth_page import engine
from auth_page.models import User
from user_page.models import User as UserInfo
from tobaccopoisk import utils

def user(request, login):
	auth = engine.getAuthorized(request)
	
	if auth != None:
		auth_login = auth.login
	else:
		auth_login = None

	isHost = auth_login == login

	users = User.objects.filter(login=login)
	if len(users) == 0:
		return render(request, 'error_404.html', {})

	user_info = UserInfo.objects.filter(auth_id=users[0])
	if len(user_info) == 0:
		return render(request, 'error_404.html', {})

	avatar = None

	if user_info[0].avatar != None and len(user_info[0].avatar.name):
		avatar = utils.image_url_handler(user_info[0].avatar.name)

	context = {'user' : users[0],
			   'isHost' : isHost,
			   'login' : auth_login,
			   'user_info' : user_info[0],
			   'avatar' : avatar}

	return render(request, 'user_page/user_page.html', context)
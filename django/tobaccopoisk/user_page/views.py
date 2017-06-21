from django.shortcuts import render
from auth_page import engine
from auth_page.models import User

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

	context = {'user' : users[0],
			   'isHost' : isHost,
			   'login' : auth_login}

	return render(request, 'user_page/user_page.html', context)
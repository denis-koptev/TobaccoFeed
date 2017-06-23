from django.shortcuts import render, redirect
from auth_page.models import Unuser, User
from auth_page import engine
from auth_page import crypto
from user_page.models import User as UserInfo
from validate_email import validate_email
from django.db import IntegrityError
from django.contrib import messages


def auth(request):

	if request.method == 'POST':

		ident = request.POST.get('login')
		password = request.POST.get('password')

		user = engine.authentication(ident, password)

		if user is None:
			return render(request, 'auth_page/auth_page.html', {'message' : 'Login or password is wrong'})

		session = engine.authorization(user)

		if session is None:
			return render(request, 'auth_page/auth_page.html', {'message' : 'Session set up failed'})

		# overwrite this
		response = redirect('/')

		# set cookies
		response.set_cookie('tfuserid', str(user.id))
		response.set_cookie('tfsession', str(session.token))
		
		return response

	else:
		return render(request, 'auth_page/auth_page.html', {})


def reg(request):
	if request.method == 'POST':
		login = request.POST.get('login')
		password = request.POST.get('password')
		mail = request.POST.get('email')

		error_msg = ""

		if engine.login_exists(login) or engine.waiting_login_exists(login):
			error_msg += "This login is not free. "

		if engine.email_exists(mail) or engine.waiting_email_exists(mail):
			error_msg += "This email was used. "

		if len(error_msg) != 0:
			return render(request, 'auth_page/reg_page.html', {'message' : error_msg})

		# create new Unuser
		passwd = crypto.hashpw(password)

		i = 5
		while i > 0:
			try:
				token = crypto.gentoken()
				unuser = Unuser(login=login, password=passwd, mail=mail, token=token)
				unuser.save()
			except IntegrityError as ex:
				# prevent token unique constraint error
				i -= 1
			else:
				engine.send_confirmation_mail(mail, token)
				break

		messages.add_message(request, messages.INFO, "Check your mail for confirmation")
		return redirect('/')
		#return render(request, 'main_page/main_page.html', {'message' : 'Check your mail for confirmation'})

	else:
		return render(request, 'auth_page/reg_page.html', {})

def mail_confirmation(request, token):

	try:
		u = Unuser.objects.get(token=token)
	except Unuser.DoesNotExist:
		# entry with this token not found
		return render(request, 'error_404.html', {})
	else:
		user = User(login=u.login, password=u.password, mail=u.mail)
		user.save()
		u.delete()
		user_info = UserInfo(auth_id=user)
		user_info.save()
		# mail confirmed message
		return redirect('/auth')
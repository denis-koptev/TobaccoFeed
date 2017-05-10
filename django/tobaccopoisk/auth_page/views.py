from django.shortcuts import render, redirect
from auth_page.models import Unuser, User
from auth_page import engine
from auth_page import crypto
from validate_email import validate_email
from django.db import IntegrityError

def auth(request):

	if request.method == 'POST':

		ident = request.POST.get('login')
		password = request.POST.get('password')

		user = engine.authentication(ident, password)

		if user is None:
			# user not found
			# RETURN FALSE
			return render(request, 'auth_page/auth_page.html', {})

		session = engine.authorization(user)

		if session is None:
			# cant craete session
			# 	should never happen
			# RETURN FALSE
			return render(request, 'auth_page/auth_page.html', {})

		# overwrite this
		response = redirect('/main')
		# set coockies
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


		if not validate_email(mail):
			# email is not valid
			# RETURN FALSE
			return render(request, 'auth_page/reg_page.html', {})


		# Check that login is free
		# in Unverified users table
		try:
			u = Unuser.objects.get(login=login)
		except Unuser.DoesNotExist:
			# user login not found. that is good. it is free.
			pass
		else:
			# this login is already in use
			# RETURN FALSE
			return render(request, 'auth_page/reg_page.html', {})

		# Check that login is free
		# in Verified users table
		try:
			u = User.objects.get(login=login)
		except User.DoesNotExist:
			# user login not found. that is good. it is free.
			pass
		else:
			# this login is already in use
			# RETURN FALSE
			return render(request, 'auth_page/reg_page.html', {})

		# Check that mail is free
		# in Unverified users table
		try:
			u = Unuser.objects.get(mail=mail)
		except Unuser.DoesNotExist:
			# user mail not found. that is good. it is free.
			pass
		else:
			# this mail is already in use
			# RETURN FALSE
			return render(request, 'auth_page/reg_page.html', {})

		# Check that mail is free
		# in Verified users table
		try:
			u = User.objects.get(mail=mail)
		except User.DoesNotExist:
			# user mail not found. that is good. it is free.
			pass
		else:
			# this mail is already in use
			# RETURN FALSE
			return render(request, 'auth_page/reg_page.html', {})


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

		# return "now check ur email to confirm registration." 
		return redirect('/main')

	else:
		return render(request, 'auth_page/reg_page.html', {})

def mail_confirmation(request, token):

	try:
		u = Unuser.objects.get(token=token)
	except Unuser.DoesNotExist:
		# entry with this token not found
		return render('404.html')
	else:
		user = User(login=u.login, password=u.password, mail=u.mail)
		user.save()
		u.delete()
		# mail confirmed message
		return redirect('/auth')
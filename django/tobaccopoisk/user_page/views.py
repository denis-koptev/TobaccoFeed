from django.shortcuts import render, HttpResponseRedirect
from auth_page import engine
from auth_page.models import User
from user_page.models import User as UserInfo
from tobaccopoisk import utils
from django.db import models
from django import forms

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

def template_upload(request, login, path):

	auth = engine.getAuthorized(request)
	if auth.login != login:
		return render(request, 'error_404.html', {})

	users = User.objects.filter(login=login)
	if len(users) == 0:
		return render(request, 'error_404.html', {})

	user_info = UserInfo.objects.filter(auth_id=users[0])
	if len(user_info) == 0:
		return render(request, 'error_404.html', {})

	context = {'user' : users[0],
			   'login' : auth.login,
			   'user_info' : user_info[0]}

	return render(request, path, context)

def edit_bio(request, login):
	auth = engine.getAuthorized(request)

	if request.method == 'POST':

		new_name = request.POST.get("name")
		if len(new_name) == 0:
			new_name = None

		new_b_date = request.POST.get("birth")
		if len(new_b_date) == 0:
			new_b_date = None

		new_place = request.POST.get("location")
		if len(new_place) == 0:
			new_place = None

		try:
			user_info = UserInfo.objects.get(auth_id=auth)
			user_info.name = new_name
			user_info.place = new_place
			user_info.b_date = new_b_date
			user_info.save()
		except BaseException:
			print("[ERROR] User update failed")
		return HttpResponseRedirect('/user/' + login)

	return template_upload(request, login, 'user_page/edit_bio.html')

def avatar_upload(request, login):
	auth = engine.getAuthorized(request)

	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid(): # this is avatar uploading
			user_info = UserInfo.objects.get(auth_id=auth)
			user_info.avatar = form.cleaned_data['image']
			user_info.save()
		return HttpResponseRedirect('/user/' + login)

	return template_upload(request, login, 'user_page/avatar_upload.html')

class ImageUploadForm(forms.Form):
	image = forms.ImageField()
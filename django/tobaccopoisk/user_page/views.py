from django.shortcuts import render, HttpResponseRedirect
from auth_page import engine
from auth_page.models import User
from user_page.models import User as UserInfo
from user_page.models import Follow
from tobaccopoisk import utils
from django import forms

def user(request, login):

	auth = engine.getAuthorized(request)

	if request.method == 'POST':

		if request.POST.get("event") == "log_out":
			print("LOGOUT")
			return engine.unauthorize(request)

		elif request.POST.get("event") == "avatar_upload":
			form = ImageUploadForm(request.POST, request.FILES)
			if form.is_valid(): # this is avatar uploading
				user_info = UserInfo.objects.get(auth_id=auth)
				user_info.avatar = form.cleaned_data['image']
				user_info.save()
			return HttpResponseRedirect('/user/' + login)

		elif request.POST.get("event") == "edit_bio":
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

	# -------------------------
	# Follow / Unfollow Routine
	# -------------------------
	is_follow = None

	if request.method == 'POST':

		if request.POST.get("event") == "follow" and isHost is False:
			is_follow = True
			try:
				follow = Follow(follower=auth, following=users[0])
				follow.save()
			except IntegrityError:
				print("[ERROR] Follow entity already exists")
			# must be here to avoid form sending after reload
			return HttpResponseRedirect('/user/' + login)

		elif request.POST.get("event") == "unfollow":
			is_follow = False
			try:
				follow = Follow.objects.filter(follower=auth, following=users[0]).delete()
			except ValueError:
				print("[ERROR] Follow entity doesn't exist")
			return HttpResponseRedirect('/user/' + login)

	if is_follow is None:
		flw = Follow.objects.filter(follower=auth, following=users[0])
		if len(flw) == 0:
			is_follow = False
		else:
			is_follow = True

	# --------
	# Response
	# --------
	context = {'user' : users[0],
			   'isHost' : isHost,
			   'login' : auth_login,
			   'user_info' : user_info[0],
			   'is_follow' : is_follow}

	return render(request, 'user_page/user_page.html', context)

def template_upload(request, login, path):

	auth = engine.getAuthorized(request)
	if auth == None or auth.login != login:
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
	if request.method == 'POST':
		if request.POST.get("event") == "log_out":
			request.path = '/user/' + login
			return engine.unauthorize(request)

	return template_upload(request, login, 'user_page/edit_bio.html')

def avatar_upload(request, login):
	if request.method == 'POST':
		if request.POST.get("event") == "log_out":
			request.path = '/user/' + login
			return engine.unauthorize(request)

	return template_upload(request, login, 'user_page/avatar_upload.html')

class ImageUploadForm(forms.Form):
	image = forms.ImageField()
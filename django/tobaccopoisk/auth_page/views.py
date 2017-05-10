from django.shortcuts import render

def auth(request):
	return render(request, 'auth_page/auth_page.html', {})

def reg(request):
	return render(request, 'auth_page/reg_page.html', {})
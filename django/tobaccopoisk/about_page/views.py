from django.shortcuts import render
from django.http import HttpResponse
from auth_page import engine

# Create your views here.

def index(request):
	if request.method == 'POST':
		return engine.unauthorize(request)

	login = engine.getAuthorized(request)

	context = {'login' : login}
	
	return render(request, 'about_page/about_page.html', context)

def error_404(request):
	return render(request, 'error_404.html', {})

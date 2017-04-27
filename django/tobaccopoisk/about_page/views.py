from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'about_page/about_page.html', {})

def error_404(request):
	return render(request, 'error_404.html', {})

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'main_page/main_page.html', {})

def error_404(request):
	return render(request, 'error_404.html', {})

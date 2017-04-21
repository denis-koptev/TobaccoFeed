from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'main_page/main_page.html', {})

def hookah(request):
    return render(request, 'main_page/hookah.html', {})

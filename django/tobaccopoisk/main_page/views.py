from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    return HttpResponse("<p><center>TobaccoPoisk.ru</center></p>")

def hookah(request):
    return render(request, 'main_page/hookah.html', {})

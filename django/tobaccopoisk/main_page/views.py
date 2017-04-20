from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<p><center>Hello, world. You're on the main page.</center></p>")
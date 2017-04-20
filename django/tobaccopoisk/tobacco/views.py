from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def tobacco_view(request, brand, name):
    return HttpResponse("<p>" + brand + "</p><br><p>" + name + "</p>")
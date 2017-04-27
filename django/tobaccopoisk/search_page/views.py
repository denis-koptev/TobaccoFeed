import json
from django.http import HttpResponse
from tobacco.models import Tobacco
from django.shortcuts import redirect
from .engine import search as do_search
from django.shortcuts import render

def search(request):
	q = request.GET.get('q')
	
	filtered = do_search(q)

	if len(filtered) == 1:
		return redirect("/" + filtered[0]["brand"].lower().replace(' ', '_') + "/" + filtered[0]["name"].lower().replace(' ', '_'))

	context = {'found': filtered}
	return render(request, 'search_page/search_page.html', context)
from .engine import search as do_search
from django.shortcuts import render, redirect
from tobaccopoisk import utils

def search(request):
	q = request.GET.get('q')
	
	filtered = do_search(q)

	if len(filtered) == 1:
		return redirect("/" + utils.to_db_str(filtered[0]["brand"]) + "/" + utils.to_db_str(filtered[0]["name"]))

	context = {'found': filtered}
	return render(request, 'search_page/search_page.html', context)
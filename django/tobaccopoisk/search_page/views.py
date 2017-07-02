from .engine import search as do_search
from django.shortcuts import render, redirect
from tobaccopoisk import utils
from auth_page import engine

def search(request):

	if request.method == 'POST':
		if request.POST.get("event") == "log_out":
			return engine.unauthorize(request)

	q = request.GET.get('q')
	
	filtered = do_search(q)

	if len(filtered) == 1:
		return redirect("/" + utils.to_db_str(filtered[0]["brand"]) + "/" + utils.to_db_str(filtered[0]["name"]))

	login = engine.getAuthorized(request)

	context = {'found': filtered,
			   'search_string': q,
			   'login' : login}
	return render(request, 'search_page/search_page.html', context)
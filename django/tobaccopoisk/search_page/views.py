from .engine import search as do_search
from django.shortcuts import render, redirect
from tobaccopoisk import utils
from auth_page import engine
from math import ceil

page_size = 10

def search(request):

	if request.method == 'POST':
		if request.POST.get("event") == "log_out":
			return engine.unauthorize(request)

	q = request.GET.get('q')
	
	filtered = do_search(q)

	if len(filtered) == 1:
		return redirect("/" + utils.to_db_str(filtered[0]["brand"]) + "/" + utils.to_db_str(filtered[0]["name"]))

	login = engine.getAuthorized(request)

	context = {'found': get_page(filtered, 0),
			   'search_string': q,
			   'login' : login,
			   'page_num' : 1,
			   'pages_all' : ceil(len(filtered) / page_size),
			   'pages_remained' : ceil(len(filtered) / page_size) - 1,
			   'total_count' : len(filtered) }
	return render(request, 'search_page/search_page.html', context)

def get_page(list, page_num):
	if (page_num + 1) * page_size > len(list):
		return list[(page_num - 1) * page_size + page_size : len(list)]
	else:
		return list[(page_num - 1) * page_size + page_size : (page_num + 1) * page_size]
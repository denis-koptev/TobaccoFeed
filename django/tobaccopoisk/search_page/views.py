from .engine import search as do_search
from django.shortcuts import render, redirect
from tobaccopoisk import utils
from auth_page import engine
from math import ceil

pageSize = 10


def search(request):

    if request.method == 'POST':
        if request.POST.get("event") == "log_out":
            return engine.unauthorize(request)

    q = request.GET.get('q')

    try:
        page = int(request.GET.get('page'))
    except ValueError:
        page = 1

    if q is None:
        q = ""

    if page is None or page < 1:
        page = 1

    filtered = do_search(q)

    if len(filtered) == 1:
        return redirect("/" + utils.to_db_str(filtered[0]["brand"]) + "/" + utils.to_db_str(filtered[0]["name"]))

    pageCount = ceil(len(filtered) / pageSize)

    if page > pageCount:
        page = pageCount

    login = engine.getAuthorized(request)

    context = {'found': getPage(filtered, page),
               'q': q,
               'login': login,
               'page': page,
               'page_count': pageCount,
               'total_count': len(filtered)}

    return render(request, 'search_page/search_page.html', context)


def getPage(list, page):

    if len(list) == 0:
        return []

    tail = pageSize * page

    if tail > len(list):
        tail = len(list)

    return list[(page - 1) * pageSize: page * pageSize]

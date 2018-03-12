from django.shortcuts import render
from tobacco_page.models import Tobacco, Mix
from search_page.engine import to_dict
from auth_page.models import User, Session
from auth_page import engine
from django.contrib.messages import get_messages


def get_last(count):
    try:
        last = Tobacco.objects.all().order_by("-id").values_list('brand', 'name', 'image')[:count]

    except Tobacco.DoesNotExist:
        return []

    return [to_dict(rec) for rec in last]


def main(request):

    if request.method == 'POST':
        if request.POST.get("event") == "log_out":
            return engine.unauthorize(request)

    login = engine.getAuthorized(request)

    message = ""
    messages = get_messages(request)
    for curr in messages:
        message = curr
        break

    mixes = Mix.objects.all().order_by('-rating')[:3]

    context = {'latest': get_last(5),
               'login': login,
               'message': str(message),
               'mixes': mixes}

    return render(request, 'main_page/main_page.html', context)

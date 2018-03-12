from django.shortcuts import render
from .models import Tobacco
from .models import Tag
from tobaccopoisk import utils
from auth_page import engine
from .models import Mix
from user_page.models import UserTobacco as UTO


def tobacco_view(request, brand, name):

    if request.method == 'POST':
        if request.POST.get("event") == "log_out":
            return engine.unauthorize(request)

    try:
        tobacco = Tobacco.objects.get(brand=brand, name=name)
    except Tobacco.DoesNotExist:
        return render(request, 'error_404.html', {})

    try:
        tags = Tag.objects.filter(tobacco=tobacco)
    except Tag.DoesNotExist:
        tags = []

    mixes = Mix.objects.filter(tobaccos=tobacco).order_by('-rating')

    login = engine.getAuthorized(request)

    utos = uto = None
    if (login is not None):
        utos = UTO.objects.filter(user=login, tobacco=tobacco)
        if len(utos) != 0:
            uto = utos[0]

    context = {'brand': utils.to_view_str(brand),
               'name': utils.to_view_str(name),
               'tobacco': tobacco,
               'image': utils.image_url_handler(tobacco.image.name),
               'tags': tags,
               'login': login,
               'mixes': mixes,
               'uto': uto}

    return render(request, 'tobacco_page/tobacco_page.html', context)

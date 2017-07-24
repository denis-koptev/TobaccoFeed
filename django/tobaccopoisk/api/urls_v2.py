from django.conf.urls import url

from . import views_v2 as api

urlpatterns = [

    url(r'^users$', api.users, name='api_v2_users'),
    url(r'^users/(?P<username>[0-9a-z-_]+)$', api.user, name='api_v2_user'),

    url(r'^tobaccos$', api.tobaccos, name='api_v2_tobaccos'),
    url(r'^tobaccos/(?P<tid>[0-9]+)$', api.tobacco, name='api_v2_tobacco'),
    url(r'^tobaccos/(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)$', api.tobacco, name='api_v2_tobacco'),

    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos$', api.utos, name='api_v2_utos'),
    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos/(?P<tid>[0-9]+)$', api.uto, name='api_v2_uto'),
    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos/(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)$', api.uto, name='api_v2_uto'),

]
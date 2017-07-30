from django.conf.urls import url

from . import views_v2 as api

urlpatterns = [

    url(r'^users$', api.users, name='api_v2_users'),
    url(r'^users/(?P<username>[0-9a-z-_]+)$', api.user, name='api_v2_user'),

    url(r'^tobaccos$', api.tobaccos, name='api_v2_tobaccos'),
    url(r'^tobaccos/(?P<tid>[0-9]+)$', api.tobacco, name='api_v2_tobacco'),
    url(r'^tobaccos/(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)$', api.tobacco, name='api_v2_tobacco'),

    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos$', api.spec_utos, name='api_v2_spec_utos'),
    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos/(?P<tid>[0-9]+)$', api.uto_get, name='api_v2_uto'),
    url(r'^users/(?P<username>[0-9a-z-_]+)/tobaccos/(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)$', api.uto_get, name='api_v2_uto'),

    url(r'^utos$', api.utos, name='api_v2_utos'),
    url(r'^umos$', api.umos, name='api_v2_umos'),
	url(r'^ufos$', api.ufos, name='api_v2_ufos'),
    
    
]

'''
    [GET]    umo?user=<str>&brands=<str,...>&tobacconame=<str,...>
    [POST]   umo?token=<str>&mix_id=<int>   
    [DELETE] umo?token=<str>&mix_id=<int>
'''
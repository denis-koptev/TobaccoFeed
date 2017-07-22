from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)([/]?)$', views.tobacco, name='api_tobacco'),
    url(r'^search$', views.search, name='api_search'),

    # ------------------------
    # UserTobacco Object API
    #

    url(r'^get_usertobacco_by_names/(?P<username>[0-9a-z-_]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)$', 
    	views.get_usertobacco_by_names, name='api_get_usertobacco_by_names'),
    url(r'^set_usertobacco_heat/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_heat, name='api_set_usertobacco_heat'),
    url(r'^set_usertobacco_strength/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_strength, name='api_set_usertobacco_strength'),
    url(r'^set_usertobacco_smoke/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_smoke, name='api_set_usertobacco_smoke'),
    url(r'^set_usertobacco_taste/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_taste, name='api_set_usertobacco_taste'),
    url(r'^set_usertobacco_rating/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_rating, name='api_set_usertobacco_rating'),
    url(r'^set_usertobacco_favorite/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_favorite, name='api_set_usertobacco_favorite'),
    url(r'^set_usertobacco_bookmark/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
    	views.set_usertobacco_bookmark, name='api_set_usertobacco_bookmark'),

    # --------------------
    # UserMix Object API
    #

    url(r'^get_usermix/(?P<username>[0-9a-z-_]+)/(?P<mix_id>[0-9]+)$', views.get_usermix, name='api_get_usermix'),
    url(r'^set_usermix_rating/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_usermix_rating, name='api_set_usermix_rating'),
    url(r'^set_usermix_favorite/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_usermix_favorite, name='api_set_usermix_favorite'),
    url(r'^set_usermix_bookmark/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_usermix_bookmark, name='api_set_usermix_bookmark'),

    # ----------
    # User API
    #

    url(r'^user_api/follow/(?P<token>[0-9a-zA-Z./]+)/(?P<username>[0-9a-z-_]+)$', views.userapi_follow, name='api_userapi_follow'),
    url(r'^user_api/is_follow/(?P<follower>[0-9a-z-_]+)/(?P<following>[0-9a-z-_]+)$', views.userapi_is_follow, name='api_userapi_is_follow'),
]
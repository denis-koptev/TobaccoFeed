from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^search$', views.search, name='api_search'),

    # ----------
    # Tobacco API
    # ----------

    url(r'^tobacco_api/get_tobacco/(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)([/]?)$', views.tobacco, name='api_tobacco'),
    url(r'^tobacco_api/recalc_tobacco_votes$',
        views.recalc_tobacco_votes, name='tobacco_api_recalc_tobacco_votes'),
    url(r'^tobacco_api/recalc_mix_votes$',
        views.recalc_mix_votes, name='tobacco_api_recalc_mix_votes'),

    # ----------
    # User API
    # ----------

    # Follow

    url(r'^user_api/follow/(?P<token>[0-9a-zA-Z./]+)/(?P<username>[0-9a-z-_]+)$', 
        views.userapi_follow,       name='api_userapi_follow'),
    url(r'^user_api/is_follow/(?P<follower>[0-9a-z-_]+)/(?P<following>[0-9a-z-_]+)$', 
        views.userapi_is_follow,    name='api_userapi_is_follow'),
    url(r'^user_api/unfollow/(?P<token>[0-9a-zA-Z./]+)/(?P<username>[0-9a-z-_]+)$', 
        views.userapi_unfollow,     name='api_userapi_unfollow'),


    # UTO

    url(r'^user_api/get_uto_by_names/(?P<username>[0-9a-z-_]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)$', 
        views.get_uto_by_names, name='api_userapi_get_uto_by_names'),
    url(r'^user_api/set_uto_heat/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_heat,     name='api_userapi_set_uto_heat'),
    url(r'^user_api/set_uto_strength/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_strength, name='api_userapi_set_uto_strength'),
    url(r'^user_api/set_uto_smoke/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_smoke,    name='api_userapi_set_uto_smoke'),
    url(r'^user_api/set_uto_taste/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_taste,    name='api_userapi_set_uto_taste'),
    url(r'^user_api/set_uto_rating/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_rating,   name='api_userapi_set_uto_rating'),
    url(r'^user_api/set_uto_favorite/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_favorite, name='api_userapi_set_uto_favorite'),
    url(r'^user_api/set_uto_bookmark/(?P<token>[0-9a-zA-Z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)/(?P<vote>[0-9]+)$', 
        views.set_uto_bookmark, name='api_userapi_set_uto_bookmark'),


    # UMO

    url(r'^user_api/get_umo/(?P<username>[0-9a-z-_]+)/(?P<mix_id>[0-9]+)$', 
        views.get_umo,          name='api_get_umo'),
    url(r'^user_api/set_umo_rating/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_umo_rating,   name='api_set_uumo_rating'),
    url(r'^user_api/set_umo_favorite/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_umo_favorite, name='api_set_umo_favorite'),
    url(r'^user_api/set_umo_bookmark/(?P<token>[0-9a-zA-Z./]+)/(?P<mix_id>[0-9]+)/(?P<vote>[0-9]+)$', 
        views.set_umo_bookmark, name='api_set_umo_bookmark'),
]
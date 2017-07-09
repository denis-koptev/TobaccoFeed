from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)([/]?)$', views.tobacco, name='api_tobacco'),
    url(r'^search$', views.search, name='api_search'),

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
]
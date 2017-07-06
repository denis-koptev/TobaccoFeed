from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)([/]?)$', views.tobacco, name='api_tobacco'),
    url(r'^search$', views.search, name='api_search'),

    url(r'^get_usertobacco_by_names/(?P<username>[0-9a-z-_]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)$', 
    	views.get_usertobacco_by_names, name='api_get_usertobacco_by_names'),
    url(r'^set_usertobacco_heat/(?P<token>[0-9a-z./]+)/(?P<brand>[0-9a-z-_]+)/(?P<tobacco>[0-9a-z-_]+)$', 
    	views.set_usertobacco_heat, name='api_set_usertobacco_heat'),
]
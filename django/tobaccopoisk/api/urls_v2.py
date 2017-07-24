from django.conf.urls import url

from . import views_v2 as api

urlpatterns = [

    url(r'^users$', api.users, name='api_v2_users'),
    url(r'^users/(?P<username>[0-9a-z-_]+)$', api.user, name='api_v2_user'),

    url(r'^tobaccos$', api.tobaccos, name='api_v2_tobaccos'),

]
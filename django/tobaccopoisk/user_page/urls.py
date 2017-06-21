from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<login>[0-9A-Za-z-_]+)([/]?)$', views.user, name='user'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[0-9a-z-_]+)/(?P<name>[0-9a-z-_]+)([/]?)$', views.tobacco, name='tobacco'),
]
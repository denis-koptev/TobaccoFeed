from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[0-9A-Za-z-_]+)/(?P<name>[0-9A-Za-z-_]+)([/]?)$', views.tobacco_view, name='tobacco_view'),
]

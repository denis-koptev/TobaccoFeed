from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[0-9a-z-]+)/(?P<name>[0-9a-z-]+)([/]?)$', views.tobacco_view, name='tobacco_view'),
]
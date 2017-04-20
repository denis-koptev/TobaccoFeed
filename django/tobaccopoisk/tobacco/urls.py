from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<brand>[a-z-]+)/(?P<name>[a-z-]+)/$', views.tobacco_view, name='tobacco_view'),
]
from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^(?P<brand>[0-9a-z-]+)/(?P<name>[0-9a-z-]+)([/]?)$', views.tobacco, name='tobacco'),
]
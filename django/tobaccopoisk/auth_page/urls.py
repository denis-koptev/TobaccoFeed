from django.conf.urls import url

from . import views

app_name = 'auth_page'

urlpatterns = [
    url(r'^(?P<token>[0-9a-zA-Z-_?.]+)$', views.mail_confirmation, name='confirm'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^auth$', views.auth, name='auth'),
]
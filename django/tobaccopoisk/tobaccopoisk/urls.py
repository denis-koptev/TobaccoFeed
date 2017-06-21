"""tobaccopoisk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import auth_page.views as auth_views
import about_page.views as about_views
import search_page.views as search_views
import main_page.views as main_views
import user_page.views as user_views

urlpatterns = [
	url(r'^$', about_views.index, name="about_page"),
    url(r'^admin[/]?', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^search$', search_views.search, name='search_page'),
    url(r'^main$', main_views.main, name='main_page'),
    url(r'^user/', user_views.user, name='user_page'),
    url(r'^reg$', auth_views.reg, name='reg_page'),
    url(r'^auth$', auth_views.auth, name='auth_page'),
    url(r'^auth/validate/(?P<token>[0-9a-zA-Z-_?./]+)$', auth_views.mail_confirmation, name='confirm'),
    
    # must be the last, motherfucker!!! 
    # DO NOT CHANGE ITS DESTINATION, BITCH
	url(r'^', include('tobacco_page.urls')),

    url(r'^', about_views.error_404, name='error_404'),
]

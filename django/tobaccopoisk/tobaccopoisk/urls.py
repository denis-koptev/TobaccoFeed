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
import main_page.views as main_view

urlpatterns = [
	url(r'^$', main_view.index, name="main_page"),
    url(r'^admin[/]?', admin.site.urls),

    # must be the last, motherfucker!!! 
    # DO NOT CHANGE ITS DESTINATION, BITCH
	url(r'^', include('tobacco.urls')),

    url(r'^', main_view.error_404, name='error_404'),
]

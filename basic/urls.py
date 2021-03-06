"""weixin URL Configuration

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
from django.conf.urls import url
from . import views

app_name = 'basic'
urlpatterns = [
    url(r'^Token/$', views.Token, name='Token'),
	url(r'^getToken/$', views.getToken, name='getToken'),
    url(r'^test/', views.test, name='test'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^scanQRCode/$', views.scanQRCode, name='scanQRCode'),
    url(r'^login/$', views.login, name='login'),
    url(r'^getCodeUrl/$', views.getCodeUrl, name='getCodeUrl'),

    url(r'^error', views.error, name='error'),
]

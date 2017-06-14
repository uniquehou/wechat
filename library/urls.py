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

app_name = 'library'
urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^index', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^classification$', views.classification, name='classification'),
    url(r'^book_detail', views.book_detail, name='book_detail'),
    url(r'^user', views.user, name='user'),
    url(r'^login', views.login, name='login'),
    url(r'^favorite', views.favorite, name='favorite'),
    url(r'^borrow$', views.borrow, name='borrow'),
    url(r'^borrow_column', views.borrow_column, name='borrow_column'),
    url(r'^backbook', views.backbook, name='backbook'),
]
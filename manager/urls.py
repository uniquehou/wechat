from django.conf.urls import url
from . import views

app_name = 'manager'
urlpatterns = [
#    url(r'^borrow$', views.borrow, name='borrow'),
#    url(r'^backbook$', views.backbook, name='backbook'),
    url(r'^user$', views.user, name='user'),
]


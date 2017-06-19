from django.conf.urls import url
from . import views

app_name = "user"
urlpatterns = [
    url(r'^user', views.user, name='user'),
    url(r'^login$', views.login, name='login'),
    url(r'^favorite', views.favorite, name='favorite'),
    url(r'^borrow_column', views.borrow_column, name='borrow_column'),
    url(r'^backbook', views.backbook, name='backbook'),
    url(r'^order', views.order, name='order'),
    url(r'^information', views.information, name='information'),
]

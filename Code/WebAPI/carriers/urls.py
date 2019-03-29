from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^airports/(?P<code>[A-Z0-9]{2})/$', views.airports, name='airports')
]
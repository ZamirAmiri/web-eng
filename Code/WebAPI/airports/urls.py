from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carriers/(?P<code>[A-Z0-9]{3})/$', views.carriers, name='carriers'),
    url(r'^carriers/(?P<a_code>[A-Z]{3})/(?P<c_code>[A-Z0-9]{2})/$', views.details, name='details'),
    url(r'^carriers/(?P<a_code>[A-Z]{3})/(?P<c_code>[A-Z0-9]{2})/date/(?P<month>\d+)/(?P<year>\d+)/$', views.monthly, name='monthly_stats')
]
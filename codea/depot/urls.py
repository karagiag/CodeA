from django.conf.urls import url

from . import views

app_name = 'depot'

urlpatterns = [ url(r'^depot/$', views.depot, name = 'depot'), ]

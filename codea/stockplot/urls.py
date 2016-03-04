from django.conf.urls import url

from . import views

app_name = 'stockplot'

urlpatterns = [ url(r'^$', views.index, name = 'index'),
                url(r'^stockapp', views.stockapp, name = 'stockapp'),]

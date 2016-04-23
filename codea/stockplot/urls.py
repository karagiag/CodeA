from django.conf.urls import url
from django.conf.urls import include
from stockplot.views import StockAutocomplete, DepotAutocomplete

from . import views

app_name = 'stockplot'

urlpatterns = [ url(r'^$', views.index, name = 'index'),
                url(r'^news/$', views.news, name = 'news'),
                url(r'^stockapp/$', views.stockapp, name = 'stockapp'),
                url(r'^depot/$', views.depot, name = 'depot'),
                url(r'^depot/buystock/$', views.buystock, name = 'buystock'),
                url(r'^depot/sellstock/$', views.sellstock, name = 'sellstock'),
                url(r'^accounts/profile/$', views.profile, name = 'profile'),
                url(
                    r'^stockapp/stock-autocomplete/$',
                    StockAutocomplete.as_view(),
                    name='stock-autocomplete',
                ),
                url(
                    r'^depot/depot-autocomplete/$',
                    DepotAutocomplete.as_view(),
                    name='depot-autocomplete',
                ),]

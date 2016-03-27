"""codea URL Configuration
"""
from django.conf.urls import include,url
from django.contrib import admin
import django.contrib.auth.urls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^accounts/', include('registration.backends.hmac.urls')), # user registration and accounts
    url(r'^', include('stockplot.urls')),   # stockplot app
    #url(r'^', include('depot.urls')),        # depot app
    url(r'^codea-admin/', admin.site.urls), # admin-site
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

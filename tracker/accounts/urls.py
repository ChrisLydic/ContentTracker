"""accounts URL Configuration
"""
from django.conf.urls import url
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^accounts/login/$',  login, 'template_name'),
    url(r'^accounts/logout/$', logout, 'template_name'),
]

"""
accounts URL Configuration
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url( r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'extra_context': { 'next': '/' } }, name='login' ),
    url( r'^logout/$', auth_views.logout, { 'next_page': '/' }, name='logout' ),
    url( r'^password_change/$', auth_views.password_change, { 'template_name': 'accounts/password_change.html' }, name='password_change' ),
    url( r'^password_change_done/$', auth_views.password_change_done, { 'template_name': 'accounts/password_change_done.html' }, name='password_change_done' ),
    url( r'^register/$', views.register, name='register' ),
    url( r'^settings_change/$', views.changeSettings, name='changeSettings' ),
    url( r'^settings/$', views.viewSettings, name='settings' ),
]

"""
accounts URL Configuration
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # both login and logout redirect users to the homepage after they finish,
    # the home url's view method handles directing them to the correct page
    url( r'^login/$',
         auth_views.login,
         {'template_name': 'accounts/login.html', 'extra_context': { 'next': '/' } },
         name='login' ),

    url( r'^logout/$', auth_views.logout, { 'next_page': '/' }, name='logout' ),

    url( r'^password_change/$',
         auth_views.password_change,
         { 'template_name': 'accounts/password_change.html' },
         name='password_change' ),

    # django will go to this url after a password change,
    # so redirect to the correct url
    url( r'^password_change_done/$',
         RedirectView.as_view(url='/accounts/settings'),
         name='password_change_done' ),

    url( r'^register/$', views.register, name='register' ),
    url( r'^settings_change/$', views.changeSettings, name='changeSettings' ),
    url( r'^settings/$', views.viewSettings, name='settings' ),
]

"""accounts URL Configuration
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url( r'^login/$', auth_views.login, {name: 'login', 'template_name': 'accounts/login.html', extra_context: { next: 'next url' } } ),
    url( r'^logout/$', auth_views.logout, {name: 'logout', 'template_name': 'accounts/logout.html'}),
    url( r'^password_change/$', auth_views.password_change, {name: 'password_change', 'template_name': 'accounts/password_change.html'}),
    url( r'^password_change_done/$', auth_views.password_change_done, {name: 'password_change_done', 'template_name': 'accounts/password_change_done.html'}),
]

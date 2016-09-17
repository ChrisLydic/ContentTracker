"""tracker URL Configuration

The `urlpatterns` list routes URLs to views.

Here the urls either go to the homepage or one of the two apps.
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url( r'^accounts/', include( 'accounts.urls' ) ),
    url( r'^lists/', include( 'lists.urls' ) ),
    url( r'^$', views.home ),
]
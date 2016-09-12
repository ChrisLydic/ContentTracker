"""
list URL Configuration

URLs for viewing, creating, editing, and deleting lists and items.

Also contains URLs for sample pages.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^create/$', views.createList, name='createList' ),
    # item creation occurs in viewList
    url( r'^(\d+)/$', views.viewList, name='viewList' ),
    url( r'^(\d+)/edit/$', views.editList, name='editList' ),
    url( r'^(\d+)/delete/$', views.deleteList, name='deleteList' ),

    url( r'^(\d+)/item/(\d+)/edit/$', views.editItem, name='editItem' ),
    url( r'^(\d+)/item/(\d+)/progress/$', views.editItemProgress, name='editItemProgress' ),
    url( r'^(\d+)/item/(\d+)/move/(up|down)/$', views.moveItem, name='moveItem' ),
    url( r'^(\d+)/item/(\d+)/delete/$', views.deleteItem, name='deleteItem' ),

    url( r'^sample/(\d+)/$', views.viewSampleList, name='sampleLists' ),
]
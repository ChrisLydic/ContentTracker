from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import *

"""

"""
def register( request ):
    form = UserRegForm( data=request.POST or None )
    
    user = request.user

    if user.is_authenticated():
        return HttpResponseRedirect( '/' )

    if form.is_valid():
        username = form.cleaned_data.get( 'username' )
        email = form.cleaned_data.get( 'email' )
        password = form.cleaned_data.get( 'password' )

        user = User.objects.create_user( username, email, password )
        user.save()

        user = authenticate( username=username, password=password )
        login( request, user )

        return HttpResponseRedirect( '/' )
    
    return render( request, 'accounts/register.html', { 'form': form } )

"""

"""
@login_required
def changeSettings(request):
    user = request.user
        
    form = UserSettingsForm(data=request.POST or None, initial={
        'username': user.username,
        'email': user.email,
    }, currUser = user)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        
        user.username = username
        user.email = email
        user.save()
        
        return HttpResponseRedirect( reverse( 'settings' ) )
    
    return render( request, 'accounts/settings.html', { 'form': form } )

"""

"""
@login_required
def viewSettings(request):
    user = request.user
        
    form = UserSettingsForm(data=request.POST or None, initial={
        'username': user.username,
        'email': user.email,
    }, currUser = user)
    
    return render( request, 'accounts/settings.html', { 'form': form, 'noEdit': True } )
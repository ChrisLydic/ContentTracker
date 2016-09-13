from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import *


def register( request ):
    """
    Uses the user registration form to display form, create user account from
    valid data (on POST), or show errors if data is invalid. If the change is
    successful, user is logged in and redirected to their homepage.

    :param request: request object
    :return:        HttpResponse object
    """
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

        if user is not None:
            login( request, user )
            return HttpResponseRedirect( '/' )
    
    return render( request, 'accounts/register.html', { 'form': form } )


@login_required
def changeSettings(request):
    """
    Uses the user settings form to show current user settings, update valid
    settings (on POST), or show errors if settings are invalid. If the change
    is successful, user is redirected to the view settings page.

    :param request: request object
    :return:        HttpResponse object
    """
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


@login_required
def viewSettings(request):
    """
    This view shows a page with user info that is displayed using the user
    settings form but doesn't allow updating to occur.

    :param request: request object
    :return:        HttpResponse object
    """
    user = request.user
        
    form = UserSettingsForm(data=request.POST or None, initial={
        'username': user.username,
        'email': user.email,
    }, currUser = user)
    
    return render( request, 'accounts/settings.html',
        { 'form': form, 'noEdit': True } )

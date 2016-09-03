from django.shortcuts import render
from django.http import HttpResponseRedirect
from lists.models import List

def home( request ):
    user = request.user
    
    if user.is_authenticated():
        currLists = List.objects.filter( user=user )
        
        if not currLists:
            return HttpResponseRedirect( '/lists/create/' )
    
        return HttpResponseRedirect( '/lists/' + 
            str( currLists.order_by( 'position' ).first().pk ) + '/' )
    else:
        return render( request, 'index.html' )
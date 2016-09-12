from django.shortcuts import render
from django.http import HttpResponseRedirect
from lists.models import List

def home( request ):
    """
    Get appropriate homepage: the index if no one is logged in or if a user
    is logged in, either send them to list creation page (if they have no
    lists) or send them to the page of the first list in their lists.

    :param request: Django request object
    :return: Appropriate response object
    """
    user = request.user
    
    if user.is_authenticated():
        currLists = List.objects.filter( user=user )
        
        if not currLists:
            return HttpResponseRedirect( '/lists/create/' )
    
        return HttpResponseRedirect( '/lists/' + 
            str( currLists.order_by( 'position' ).first().pk ) + '/' )
    else:
        return render( request, 'index.html' )
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import List, Item, getItems, getItem, makeItem
from .forms import ListForm, ItemForm, LinkForm, BookForm
import json

"""

"""
@login_required
def createList( request ):
    form = ListForm( data=request.POST or None )
    user = request.user
    
    if form.is_valid():
        name = form.cleaned_data.get('name')
        progType = form.cleaned_data.get( 'progType' )
        itemType = form.cleaned_data.get( 'itemType' )
        hasDescription = form.cleaned_data.get('hasDescription')

        res = List.objects.filter( user=user )

        if res:
            currPos = res.order_by( '-position' ).first().position + 1
        else:
            currPos = 0
        
        newList = List(
            user=user,
            name=name,
            progType=progType,
            itemType=itemType,
            hasDescription=hasDescription,
            position=currPos
        )
        newList.save()
        
        return HttpResponseRedirect( '/lists/' + str( newList.pk ) + '/' )
    
    lists = List.objects.filter( user=user ).order_by( 'position' , 'dateCreated' )
    
    return render( request, 'lists/createList.html', { 'form': form, 'lists': lists, } )

"""

"""
@login_required
def viewList( request, listpk ):
    user = request.user
    currList = List.objects.get( pk=listpk, user=user )

    if currList.itemType == 'Item':
        form = ItemForm( data=request.POST or None )
    elif currList.itemType == 'Link':
        form = LinkForm( data=request.POST or None )
    elif currList.itemType == 'Book':
        form = BookForm( data=request.POST or None )
    else:
        return HttpResponseServerError( 'Item type doesn\'t exist.' )
    
    if currList is None:
        raise Http404( 'List does not exist.' )
            
    if form.is_valid():
        cleaned_data = form.cleaned_data
        
        res = Item.objects.filter( list=currList, user=user )

        if res:
            currPos = res.order_by( '-position' ).first().position + 1
        else:
            currPos = 0

        makeItem( user, currList, cleaned_data, currPos )

        return HttpResponseRedirect( '/lists/' + str( currList.pk ) + '/' )
    
    lists = List.objects.filter( user=user ).order_by( 'position' , 'dateCreated' )
    items = getItems( user, currList )
    
    return render( request, 'lists/list.html', {
        'form': form,
        'lists': lists,
        'items': items,
        'currList': currList,
    } )

"""

"""
@login_required
def editList( request, listpk ):
    user = request.user
    
    currList = List.objects.get( pk=listpk, user=user )
    
    if currList is None:
        raise Http404( 'List does not exist.' )
    
    if currList.user != user:
        return render( request, 'lists/list.html',
            { 'error': 'You are not authorized to access this list.', } )
    
    form = ListForm( data=request.POST or None, initial={
        'name': currList.name,
        'progType': currList.progType,
        'itemType': currList.itemType,
        'hasDescription': currList.hasDescription,
    } )
    
    if form.is_valid():
        name = form.cleaned_data.get('name')
        progType = form.cleaned_data.get( 'progType' )
        hasDescription = form.cleaned_data.get('hasDescription')
        
        currList.name = name
        currList.progType = progType
        currList.hasDescription = hasDescription
        currList.save()
        
        return HttpResponseRedirect( '/lists/' + str( currList.pk ) + '/' )
    
    lists = List.objects.filter( user=user ).order_by( 'position' , 'dateCreated' )
    
    return render( request, 'lists/editList.html', {
        'form': form,
        'lists': lists,
        'currList': currList,
    } )

"""

"""
@login_required
def deleteList( request, listpk ):
    user = request.user
    currList = List.objects.get( pk=listpk, user=user )
    
    if not currList:
        raise Http404( 'List does not exist.' )
    
    currList.delete()
    
    currLists = List.objects.filter( user=user )
    
    if not currLists:
        return HttpResponseRedirect( '/lists/create/' )
    
    return HttpResponseRedirect( '/lists/' + 
        str( currLists.order_by( 'position', 'dateCreated' ).first().pk ) + '/' )

"""

"""
@login_required
def editItem( request, listpk, itempk ):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        currList = List.objects.get( pk=listpk, user=user )
        currItem = getItem( user, currList, itempk )
        args = json.loads( request.body.decode('utf-8') )
        data = { 'errors': [] }

        if not currItem:
            raise Http404( 'Item does not exist.' )

        if not currList.hasDescription:
            args.update( { 'description': '' } )
        
        if currList.itemType == 'Item':
            form = ItemForm( data={
                'name': args['name'],
                'description': args['description'],
            } )

            if form.is_valid():
                currItem.name = form.cleaned_data.get( 'name' )
                currItem.description = form.cleaned_data.get( 'description' )
                itemArgs = {
                    'name': currItem.name,
                    'description': currItem.description,
                }
            else:
                for field in form:
                    if field.errors:
                        data['errors'].append( field.name.capitalize() + ': ' + field.errors.as_text() )
                return JsonResponse( data )

        elif currList.itemType == 'Link':
            form = LinkForm( data={
                'name': args['name'],
                'description': args['description'],
                'url': args['url'],
            } )

            if form.is_valid():
                currItem.name = form.cleaned_data.get( 'name' )
                currItem.description = form.cleaned_data.get( 'description' )
                currItem.url = form.cleaned_data.get( 'url' )
                itemArgs = {
                    'name': currItem.name,
                    'description': currItem.description,
                    'url': currItem.url,
                }
            else:
                for field in form:
                    if field.errors:
                        data['errors'].append( field.name.capitalize() + ': ' + field.errors.as_text() )
                return JsonResponse( data )

        else:
            return HttpResponseServerError( 'Item type doesn\'t exist.' )
        
        currItem.save()
        
        data.update( itemArgs )
        data.update( { 'itempk': itempk } )
        return JsonResponse( data )

    else:
        raise Http404

"""

"""
@login_required
def editItemProgress( request, listpk, itempk ):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        currItem = getItem( user, List.objects.get( user=user, pk=listpk ), itempk )

        if not currItem:
            raise Http404( 'Item does not exist.' )

        newProgress = request.POST.get( 'progress' )

        if currItem.progress != newProgress:
            currItem.progress = newProgress
            currItem.save()

        return JsonResponse( data={} )

    else:
        raise Http404

"""

"""
@login_required
def moveItem( request, listpk, itempk, direction ):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        currList = List.objects.get( pk=listpk )
        currItem = getItem( user, currList, itempk )

        if currItem is None:
            raise Http404( 'Item does not exist.' )

        try:
            if direction == 'down':
                aboveItem = getItems( user, currList ).filter( position__lt=( currItem.position ) ).first()
            else:
                aboveItem = getItems( user, currList ).filter( position__gt=( currItem.position ) ).last()
        except:
            # if the item is at the beginning or end of the list, don't do anything
            raise Http404( 'Item does not exist.' )

        position = aboveItem.position
        aboveItem.position = currItem.position
        currItem.position = position
        aboveItem.save()
        currItem.save()
        
        return JsonResponse( data={} )

    else:
        raise Http404

"""

"""
@login_required
def deleteItem( request, listpk, itempk ):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        currItem = getItem( user, List.objects.get( user=user, pk=listpk ), itempk )

        if not currItem:
            raise Http404( 'Item does not exist.' )
        else:
            currItem.delete()
        
        return JsonResponse( data={} )
    
    else:
        raise Http404
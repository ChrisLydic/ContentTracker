from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

def getItem( user, list, itempk ):
    itemType = list.itemType

    if itemType == 'Item':
        item = Item.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Link':
        item = Link.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Book':
        item = Book.objects.get( pk=itempk, list=list, user=user )

    return item

def getItems( user, list ):
    itemType = list.itemType

    if itemType == 'Item':
        itemSet = Item.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Link':
        itemSet = Link.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Book':
        itemSet = Book.objects.filter( list=list, user=user ).order_by( '-position' )

    return itemSet

def makeItem( user, list, cleanedData, currPos ):
    itemType = list.itemType

    if itemType == 'Item':
        newItem = Item(
            user=user,
            list=list,
            name=cleanedData.get('name'),
            description=cleanedData.get('description'),
            position=currPos
        )
        newItem.save()
    elif itemType == 'Link':
        newItem = Link(
            user=user,
            list=list,
            name=cleanedData.get('name'),
            description=cleanedData.get('description'),
            url=cleanedData.get('url'),
            position=currPos
        )
        newItem.save()
    elif itemType == 'Book':
        olid = cleanedData.get( 'olid' )
        cover = cleanedData.get( 'cover' )
        if not olid:
            olid = 'none'
        if not cover:
            cover = 'none'

        newItem = Book(
            user=user,
            list=list,
            name=cleanedData.get('name'),
            description=cleanedData.get('description'),
            olid=olid,
            cover=cover,
            pageNumber=cleanedData.get('pageNumber'),
            authors=cleanedData.get('authors'),
            position=currPos
        )
        newItem.save()

class List( models.Model ):
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    name = models.CharField( max_length=40 )
    sublist = models.BooleanField( default=False )
    
    # Used to order the lists
    dateCreated = models.DateField( auto_now_add=True )

    position = models.PositiveIntegerField()
    
    # True if item progress is measured with a progress bar, false if progress is a boolean
    progLabels = (
        ( 'none', 'Don\'t track progress' ),
        ( 'bar', 'Progress bar' ),
        ( 'check', 'Checkbox' )
    )
    progType = models.CharField( max_length=20, choices=progLabels, default='none' )
    
    # True if items have descriptions, false otherwise
    hasDescription = models.BooleanField()

    # An item class or subclass
    itemLabels = (
        ( 'Item', 'Default' ),
        ( 'Link', 'Websites' ),
        # ( 'movies', 'Movies' ),
        # ( 'tv shows', 'TV Shows' ),
        ( 'Book', 'Books' )
    )
    itemType = models.CharField( max_length=10, choices=itemLabels, default='Item' )

class Item( models.Model ):
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    list = models.ForeignKey( List, on_delete=models.CASCADE )
    dateCreated = models.DateField( auto_now_add=True )
    name = models.CharField( max_length=40 )
    description = models.CharField( max_length=500 )
    
    # Used to order the items, bottom-most item is 0
    position = models.PositiveIntegerField()
    
    # When progress is a boolean, 0 is false and any other value is true
    progress = models.PositiveIntegerField( default=0, validators=[ MaxValueValidator(100) ] )

    # keywords = models.TextField( max_length=1000 )

class Link( Item ):
    url = models.URLField( max_length=500 )

class Book( Item ):
    # open library id
    olid = models.CharField( max_length=20, default='none' )
    cover = models.URLField( max_length=500, default='none' )
    pageNumber = models.PositiveIntegerField()
    authors = models.CharField( max_length=200 )

# class Show( Item ):
#     url = models.URLField( max_length=500 )

# class Movie( Item ):
#     url = models.URLField( max_length=500 )
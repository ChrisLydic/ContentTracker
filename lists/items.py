"""
Helper functions for creating and retrieving items.
"""
from .models import Item, Link, Book, Video


def getItem( user, list, itempk ):
    """

    :param user:
    :param list:
    :param itempk:
    :return:
    """
    itemType = list.itemType

    if itemType == 'Item':
        item = Item.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Link':
        item = Link.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Book':
        item = Book.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Show' or itemType == 'Movie':
        item = Video.objects.get( pk=itempk, list=list, user=user )

    return item


def getItems( user, list ):
    """

    :param user:
    :param list:
    :return:
    """
    itemType = list.itemType

    if itemType == 'Item':
        itemSet = Item.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Link':
        itemSet = Link.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Book':
        itemSet = Book.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Show' or itemType == 'Movie':
        itemSet = Video.objects.filter( list=list, user=user ).order_by( '-position' )

    return itemSet


def makeItem( user, list, cleanedData, currPos ):
    """

    :param user:
    :param list:
    :param cleanedData:
    :param currPos:
    :return:
    """
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
            position=currPos,
            url=cleanedData.get('url')
        )
        newItem.save()

    elif itemType == 'Book':
        olid = cleanedData.get( 'olid' )
        cover = cleanedData.get( 'cover' )
        useOlid = True
        
        if not olid:
            useOlid = False
            olid = 'none'
            url = '/'
        else:
            url = 'https://openlibrary.org/books/' + olid

        if not cover:
            cover = 'none'

        newItem = Book(
            user=user,
            list=list,
            name=cleanedData.get('name'),
            description=cleanedData.get('description'),
            position=currPos,
            url=url,
            useOlid=useOlid,
            olid=olid,
            cover=cover,
            pageNumber=cleanedData.get('pageNumber'),
            authors=cleanedData.get('authors')
        )
        newItem.save()
    
    elif itemType == 'Show' or itemType == 'Movie':
        cover = cleanedData.get( 'cover' )
        imdbId = cleanedData.get('imdbId')
        imdbRating = cleanedData.get('imdbRating')
        metascore = cleanedData.get('metascore')
        creators = cleanedData.get('creators')
        useOmdb = True

        if not imdbId:
            useOmdb = False
            imdbId = 'none'
            imdbRating = 0
            metascore = 0

        if not cover:
            cover = 'none'
        
        if not creators:
            creators = ''

        newItem = Video(
            user=user,
            list=list,
            name=cleanedData.get('name'),
            description=cleanedData.get('description'),
            position=currPos,
            useOmdb=useOmdb,
            imdbId=imdbId,
            cover=cover,
            imdbRating=imdbRating,
            metascore=metascore,
            length=cleanedData.get('length'),
            creators=creators
        )
        newItem.save()

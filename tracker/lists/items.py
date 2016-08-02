from .models import Item, Link, Book, Show, Movie

def getItem( user, list, itempk ):
    itemType = list.itemType

    if itemType == 'Item':
        item = Item.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Link':
        item = Link.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Book':
        item = Book.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Show':
        item = Show.objects.get( pk=itempk, list=list, user=user )
    elif itemType == 'Movie':
        item = Movie.objects.get( pk=itempk, list=list, user=user )

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
            url=url,
            olid=olid,
            cover=cover,
            pageNumber=cleanedData.get('pageNumber'),
            authors=cleanedData.get('authors'),
            position=currPos
        )
        newItem.save()
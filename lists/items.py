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
    elif itemType == 'Show':
        itemSet = Show.objects.filter( list=list, user=user ).order_by( '-position' )
    elif itemType == 'Movie':
        itemSet = Movie.objects.filter( list=list, user=user ).order_by( '-position' )

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
    
    elif itemType == 'Show':
        cover = cleanedData.get( 'cover' )
        imdbId = cleanedData.get('imdbId')
        imdbRating = cleanedData.get('imdbRating')
        metascore = cleanedData.get('metascore')
        writers = cleanedData.get('writers')
        useOmdb = True

        if not imdbId:
            useOmdb = False
            imdbId = 'none'
            imdbRating = 0
            metascore = 0

        if not cover:
            cover = 'none'
        
        if not writers:
            writers = ''

        newItem = Show(
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
            seasons=cleanedData.get('seasons'),
            writers=writers
        )
        newItem.save()

    elif itemType == 'Movie':
        cover = cleanedData.get( 'cover' )
        imdbId = cleanedData.get('imdbId')
        imdbRating = cleanedData.get('imdbRating')
        metascore = cleanedData.get('metascore')
        directors = cleanedData.get('directors')
        useOmdb = True

        if not imdbId:
            useOmdb = False
            imdbId = 'none'
            imdbRating = 0
            metascore = 0
        
        if not cover:
            cover = 'none'
        
        if not directors:
            directors = ''

        newItem = Movie(
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
            runtime=cleanedData.get('runtime'),
            directors=directors
        )
        newItem.save()
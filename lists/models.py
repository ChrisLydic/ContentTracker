from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
        ( 'Movie', 'Movies' ),
        ( 'Show', 'TV Shows' ),
        ( 'Book', 'Books' )
    )
    itemType = models.CharField( max_length=10, choices=itemLabels, default='Item' )

class Item( models.Model ):
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    list = models.ForeignKey( List, on_delete=models.CASCADE )
    dateCreated = models.DateField( auto_now_add=True )
    name = models.CharField( max_length=100 )
    description = models.CharField( max_length=500, default='' )
    
    # Used to order the items, bottom-most item is 0
    position = models.PositiveIntegerField()
    
    # When progress is a boolean, 0 is false and any other value is true
    progress = models.PositiveIntegerField( default=0,
        validators=[ MaxValueValidator(100) ] )

    # keywords = models.TextField( max_length=1000 )

class Link( Item ):
    url = models.URLField( max_length=500, default='/' )

class Book( Link ):
    cover = models.URLField( max_length=2000, default='none' )
    # zero value is equal to false for pageNumber
    pageNumber = models.PositiveIntegerField( default=0 )
    authors = models.CharField( max_length=200, default='Anonymous' )

    useOlid = models.BooleanField( default=False )
    # open library id
    olid = models.CharField( max_length=20, default='none' )

class Show( Item ):
    cover = models.URLField( max_length=2000, default='none' )
    # zero value is equal to false for seasons, imdbRating, and metascore
    seasons = models.PositiveIntegerField( default=0 )
    writers = models.CharField( max_length=200, default='' )

    useOmdb = models.BooleanField( default=False )
    # used as unique id for OMDb and to link to imdb
    imdbId = models.CharField( max_length=20, default='none' )
    imdbRating = models.DecimalField( max_digits=3, decimal_places=1, default=0,
        validators=[ MaxValueValidator(10), MinValueValidator(0) ] )
    metascore = models.PositiveIntegerField( default=0,
        validators=[ MaxValueValidator(100) ] )

class Movie( Item ):
    cover = models.URLField( max_length=2000, default='none' )
    # zero value is equal to false for runtime, imdbRating, and metascore
    runtime = models.PositiveIntegerField( default=0 )
    directors = models.CharField( max_length=200, default='' )

    useOmdb = models.BooleanField( default=False )
    # used as unique id for omdb and to link to imdb
    imdbId = models.CharField( max_length=20, default='none' )
    imdbRating = models.DecimalField( max_digits=3, decimal_places=1, default=0,
        validators=[ MaxValueValidator(10), MinValueValidator(0) ] )
    metascore = models.PositiveIntegerField( default=0,
        validators=[ MaxValueValidator(100) ] )
"""
Models for List, Item, and subclasses of Item.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class List( models.Model ):
    """
    A list model mostly contains settings that apply to the items in a list.
    """
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    name = models.CharField( max_length=40 )

    # will be used for implementing sublists
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
    """
    Items have a many to one relationship with a list.
    They contain a name, description, and progress.

    Progress and description may be ignored by the html template
    depending on settings in their corresponding list.
    """
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
    """
    Links inherit all fields of the Item model and include a url field.
    URLs are displayed indirectly in an <a> tag in the html template.
    """
    url = models.URLField( max_length=500, default='/' )


class Book( Link ):
    """
    Inherits fields off Link model and Item model.

    Books can be created using data from the Open Library API.
    The useOlid field indicates whether or not the book was created in this
    way, and when the field is True there should be an Open Library ID in the
    olid field and the url field should be the url of the book's page on the
    Open Library website. The url field is only used to link to this page.
    """
    cover = models.URLField( max_length=2000, default='none' )
    # zero value is equal to false for pageNumber
    pageNumber = models.PositiveIntegerField( default=0 )
    authors = models.CharField( max_length=200, default='Anonymous' )

    useOlid = models.BooleanField( default=False )
    # open library id
    olid = models.CharField( max_length=20, default='none' )


class Video( Item ):
    """
    Inherits fields from Item model.

    Shows can be created using data from The Open Movie Database (OMDb) API.
    The useOmdb field indicates whether or not the book was created in this
    way, and if it was there will be a value in the imdbId field. Both IMDb
    and OMDb use IMDb ids to uniquely identify titles.

    A zero value is equal to false for seasons, imdbRating, and metascore
    """
    cover = models.URLField( max_length=2000, default='none' )
    # for shows this is number of seasons, for movies this is runtime
    length = models.PositiveIntegerField( default=0 )
    creators = models.CharField( max_length=200, default='' )

    useOmdb = models.BooleanField( default=False )
    # used as unique id for OMDb and to link to IMDb
    imdbId = models.CharField( max_length=20, default='none' )
    imdbRating = models.DecimalField( max_digits=3, decimal_places=1, default=0,
        validators=[ MaxValueValidator(10), MinValueValidator(0) ] )
    metascore = models.PositiveIntegerField( default=0,
        validators=[ MaxValueValidator(100) ] )

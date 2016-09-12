from django import forms
from django.contrib.auth.models import User


class ListForm(forms.Form):
    """
    Form for creating a list.
    """
    name = forms.CharField( label='Name', max_length=40, required=True )

    progLabels = (
        ( 'none', 'Don\'t track progress' ),
        ( 'bar', 'Progress bar' ),
        ( 'check', 'Checkbox' )
    )
    progType = forms.ChoiceField( label='Track Progress', choices=progLabels,
        initial='Don\'t track progress', required=True )
    
    itemLabels = (
        ( 'Item', 'Default' ),
        ( 'Link', 'Websites' ),
        ( 'Movie', 'Movies' ),
        ( 'Show', 'TV Shows' ),
        ( 'Book', 'Books' )
    )
    itemType = forms.ChoiceField( label='List Type', choices=itemLabels,
        initial='Item', required=False )

    hasDescription = forms.BooleanField( label='Show Descriptions',
        required=False, initial='True' )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault( 'label_suffix', '' )
        super( ListForm, self ).__init__( *args, **kwargs )


class ItemForm( forms.Form ):
    """
    Form for creating a normal item.
    """
    name = forms.CharField( label='Name', max_length=100, required=True )
    description = forms.CharField( label='Description', max_length=500,
        required=False )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault( 'label_suffix', '' )
        super( ItemForm, self ).__init__( *args, **kwargs )


class LinkForm( ItemForm ):
    """
    Form for creating a link item.
    """
    url = forms.URLField( label='Website', max_length=500, required=True,
        initial='http://' )


class BookForm( ItemForm ):
    """
    Form for creating a book item. Because the olid should only be assigned
    a value when the book is created through the search functionality, it is
    hidden from users.
    """
    cover = forms.URLField( label='Image URL', max_length=2000, required=False,
        widget=forms.URLInput( attrs={ 'placeholder': 'http://' } ) )
    pageNumber = forms.IntegerField( label='Number of Pages', min_value=0,
        required=True, initial='0' )
    authors = forms.CharField( label='Author(s)', max_length=200, required=True )
    olid = forms.CharField( label='', max_length=20, widget=forms.HiddenInput,
        required=False )


class ShowForm( ItemForm ):
    """
    Form for creating a tv show item. Because the imdbId, imdbRating, and
    metascore should only be assigned a value when the item is created through
    the search functionality, they are hidden from users.

    The video model is used for shows and movies, but they have different
    forms in order to show form labels that are not confusing to users.
    """
    cover = forms.URLField( label='Image URL', max_length=2000, required=False,
        widget=forms.URLInput( attrs={ 'placeholder': 'http://' } ) )
    length = forms.IntegerField( label='Seasons', min_value=0,
        required=True, initial='0' )
    creators = forms.CharField( label='Writer(s)', max_length=200, required=False )

    imdbId = forms.CharField( label='', max_length=20, widget=forms.HiddenInput,
        required=False )
    imdbRating = forms.DecimalField( label='', widget=forms.HiddenInput,
        required=False )
    metascore = forms.IntegerField( label='', widget=forms.HiddenInput,
        required=False )


class MovieForm( ItemForm ):
    """
    Form for creating a movie item. Because the imdbId, imdbRating, and
    metascore should only be assigned a value when the item is created through
    the search functionality, they are hidden from users.

    The video model is used for shows and movies, but they have different
    forms in order to show form labels that are not confusing to users.
    """
    cover = forms.URLField( label='Image URL', max_length=2000, required=False,
        widget=forms.URLInput( attrs={ 'placeholder': 'http://' } ) )
    length = forms.IntegerField( label='Runtime (minutes)', min_value=0,
        required=True, initial='0' )
    creators = forms.CharField( label='Director(s)', max_length=200, required=False )

    imdbId = forms.CharField( label='', max_length=20, widget=forms.HiddenInput,
        required=False )
    imdbRating = forms.DecimalField( label='', widget=forms.HiddenInput,
        required=False )
    metascore = forms.IntegerField( label='', widget=forms.HiddenInput,
        required=False )
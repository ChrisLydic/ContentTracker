from django import forms
from django.contrib.auth.models import User

"""
List
"""
class ListForm(forms.Form):
    name = forms.CharField( label='Name', max_length=40, required=True )

    progLabels = (
        ( 'none', 'Don\'t track progress' ),
        ( 'bar', 'Progress bar' ),
        ( 'check', 'Checkbox' )
    )
    progType = forms.ChoiceField( label='Track Progress', choices=progLabels, initial='Don\'t track progress', required=True )
    
    itemLabels = (
        ( 'Item', 'Default' ),
        ( 'Link', 'Websites' ),
        # ( 'movies', 'Movies' ),
        # ( 'tv shows', 'TV Shows' ),
        ( 'Book', 'Books' )
    )
    itemType = forms.ChoiceField( label='List Type', choices=itemLabels, initial='Item', required=False )

    hasDescription = forms.BooleanField( label='Show Descriptions', required=False, initial='True' )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault( 'label_suffix', '' )
        super( ListForm, self ).__init__( *args, **kwargs )

"""
Item
"""
class ItemForm( forms.Form ):
    name = forms.CharField( label='Name', max_length=40, required=True )
    description = forms.CharField( label='Description', max_length=500, required=False )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault( 'label_suffix', '' )
        super( ItemForm, self ).__init__( *args, **kwargs )

"""
Item
"""
class LinkForm( ItemForm ):
    url = forms.URLField( label='Website', max_length=500, required=True, initial='http://' )

"""
Item
"""
class BookForm( ItemForm ):
    cover = forms.URLField( label='Image URL', max_length=500, required=False, initial='http://' )
    pageNumber = forms.IntegerField( label='Number of Pages', min_value=0, required=True, initial='0' )
    authors = forms.CharField( label='Author(s)', max_length=200, required=True )
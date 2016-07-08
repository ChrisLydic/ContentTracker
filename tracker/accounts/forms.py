from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

"""
User registration
"""
class UserRegForm( forms.Form ):
    username = forms.CharField( label='Username', required=True, max_length=30 )
    email = forms.EmailField( label='Email', required=True, max_length=50 )
    password = forms.CharField( widget=forms.PasswordInput, label='Password', required=True )
    passwordCheck = forms.CharField( widget=forms.PasswordInput, label='Password (type again)', required=True )

    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'label_suffix', '' )
        super( UserRegForm, self ).__init__( *args, **kwargs )
    
    def clean_email( self ):
        email = self.cleaned_data.get( 'email' )
        if User.objects.filter( email=email ).exists():
            raise forms.ValidationError( 'That email address is unavailable.' )
        return email

    def clean_username( self ):
        user = self.cleaned_data.get( 'username' )
        if User.objects.filter( username=user ).exists():
            raise forms.ValidationError( 'That username is taken.' )
        return user
    
    def clean_password( self ):
        password = self.cleaned_data.get( 'password' )
        validate_password( password )
        return password

    def clean( self ):
        cleaned_data = super( UserRegForm, self ).clean()
        password = cleaned_data.get( 'password' )

        if password != None and password != cleaned_data.get( 'passwordCheck' ):
            raise forms.ValidationError( { 'passwordCheck': 'Passwords don\'t match.' } )
        return cleaned_data
        
"""
User settings
"""
class UserSettingsForm( forms.Form ):
    username = forms.CharField( label='Username', required=False )
    email = forms.EmailField( label='Email', required=False )

    def __init__( self, currUser, *args, **kwargs ):
        kwargs.setdefault( 'label_suffix', '' )
        super( UserSettingsForm, self ).__init__( *args, **kwargs )
        self.currUser = currUser

    def clean_email( self ):
        email = self.cleaned_data.get( 'email' )
        if User.objects.filter( email=email ).exists() and self.currUser.email != email:
            raise forms.ValidationError( 'That email address is unavailable.' )
        return email
    
    def clean_username( self ):
        user = self.cleaned_data.get( 'username' )
        if User.objects.filter( username=user ).exists() and self.currUser.username != user:
            raise forms.ValidationError( 'That username is taken.' )
        return user
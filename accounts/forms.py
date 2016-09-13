from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegForm( forms.Form ):
    """
    User registration form. Contains cleaning methods that handle all fields.
    Checks for unique username and email. Validates passwords with Django
    password validators.
    """
    username = forms.CharField( label='Username', required=True, max_length=30 )
    email = forms.EmailField( label='Email', required=True, max_length=50 )
    password = forms.CharField( widget=forms.PasswordInput, label='Password', required=True )
    passwordCheck = forms.CharField( widget=forms.PasswordInput, label='Password (type again)', required=True )

    def __init__( self, *args, **kwargs ):
        """
        Initializes the form by calling constructor of super class and removes
        the default label ending ":".

        :param args:
        :param kwargs:
        """
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
        """
        Runs after all individual field cleaning methods have completed.
        Checks that user entered same password in both password fields and
        raises validation error if they do not match.

        :return: the cleaned data of the form
        """
        cleaned_data = super( UserRegForm, self ).clean()
        password = cleaned_data.get( 'password' )

        if password is not None and password != cleaned_data.get( 'passwordCheck' ):
            raise forms.ValidationError( { 'passwordCheck': 'Passwords don\'t match.' } )
        return cleaned_data
        

class UserSettingsForm( forms.Form ):
    """
    User settings form, for changing username or email.
    """
    username = forms.CharField( label='Username', required=False )
    email = forms.EmailField( label='Email', required=False )

    def __init__( self, currUser, *args, **kwargs ):
        """
        Initializes the form by calling constructor of super class, removing the
        default label ending ":", and adding currUser to the form object for
        later validation.

        :param currUser: User who is changing settings
        :param args:
        :param kwargs:
        """
        kwargs.setdefault( 'label_suffix', '' )
        super( UserSettingsForm, self ).__init__( *args, **kwargs )
        self.currUser = currUser

    def clean_email( self ):
        """
        Checks if someone else is using the new email. Raises validation error if
        the email is unavailable.

        :return: cleaned email
        """
        email = self.cleaned_data.get( 'email' )
        if User.objects.filter( email=email ).exists() and self.currUser.email != email:
            raise forms.ValidationError( 'That email address is unavailable.' )
        return email
    
    def clean_username( self ):
        """
        Checks if someone else is using the new username. Raises validation
        error if the username is unavailable.

        :return: cleaned username
        """
        user = self.cleaned_data.get( 'username' )
        if User.objects.filter( username=user ).exists() and self.currUser.username != user:
            raise forms.ValidationError( 'That username is taken.' )
        return user
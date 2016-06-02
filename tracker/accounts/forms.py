from django import forms
from django.contrib.auth.models import User

"""
Account information
"""
class AccountForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        return email

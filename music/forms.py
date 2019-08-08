#imports the generic user class that we can use
from django.contrib.auth.models import User
from django import forms
from music.models import Hero

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']


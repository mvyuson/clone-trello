from django import forms
from .models import Board, List
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    first_password = forms.CharField(widget=forms.PasswordInput)
    second_password = forms.CharField(widget=forms.PasswordInput)

    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('Email already taken')
        return email

    def clean_password(self):
        first_password = self.cleaned_data['first_password']
        second_password = self.cleaned_data['second_password']
        if first_password != second_password:
            raise forms.ValidationError('Password mismatched')
        
        return first_password

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['first_password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddBoardTitleForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Board
        fields = ('title',)


class AddListForm(forms.ModelForm):
    list_title = forms.CharField(initial='')

    class Meta:
        model = List 
        fields = ('list_title',)

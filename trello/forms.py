from django import forms
from .models import Board, List
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    second_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddBoardTitleForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title',)


class AddListForm(forms.ModelForm):
    list_title = forms.CharField(initial='')

    class Meta:
        model = List 
        fields = ('list_title',)

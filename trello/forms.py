from django import forms
from .models import Board, List, Card, BoardMembers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    """
    Creates form for Sign Up. 
    """
    
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    second_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_password', 'second_password')

    def clean_email(self):
        """
        Check if email was already taken.
        """
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('Email already taken')
        return email
    
    def clean(self):
        """
        Check if passwords match.
        """
        cleaned_data = super().clean()
        first_password = cleaned_data.get("first_password")
        second_password = cleaned_data.get("second_password")

        if first_password != second_password:
            raise forms.ValidationError(
                self.add_error('second_password', "Passwords are mismatched!")
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data.get('first_password'))
            user.save()
        return user 


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        """
        Check if the username entered exitst.
        """
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            pass 
        else:
            raise forms.ValidationError('Invalid Username')

        return username


class AddBoardTitleForm(forms.ModelForm):
    """
    Create Board form.
    """
    class Meta:
        model = Board
        fields = ('title',)


class AddListForm(forms.ModelForm):
    """
    Create List form.
    """
    list_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+ Add List'})
    )

    class Meta:
        model = List 
        fields = ('list_title',)


class AddCardForm(forms.ModelForm):
    """
    Create Card form.
    """

    card_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+ Add Card'})
    )

    class Meta:
        model = Card
        fields = ('card_title',)


class AddCardDescriptionForm(forms.ModelForm):
    """
    Create Card Description form.
    """

    card_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add more detailed description...'})
    )

    class Meta:
        model = Card 
        fields = {'card_description',}


class InviteMemberForm(forms.ModelForm):
    """
    Invite Member form.
    """

    members = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        to_field_name='username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )

    class Meta:
        model = BoardMembers
        fields = {'members',}

    def clean_member(self):
        import pdb; pdb.set_trace()
        members = self.cleaned_data['members']
        board_member = BoardMembers.objects.filter(members=members)
        print(board_member.members)
        if board_member.exists():      
           raise forms.ValidationError('User was already a member.') 
        return members

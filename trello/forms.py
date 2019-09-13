from .models import Board, List, Card, BoardMembers, CardImage, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


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


class InviteMemberForm(forms.ModelForm):
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


class CardImageForm(forms.ModelForm):
    class Meta:
        model = CardImage
        fields = {'image'}


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, label='')
    class Meta: 
        model = UserProfile
        fields = ('bio', 'photo',)


class EditUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, label='')
    email = forms.CharField(widget=forms.EmailInput, label='')

    class Meta:
        model = User 
        fields = ('username', 'email')
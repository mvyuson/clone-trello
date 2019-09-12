from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_delete

from datetime import datetime


class Card(models.Model):
    """
    'board_list' is the list the card is member of
    'author' is the user who created the card
    'card_title' is the title of the card
    'created_date' automatically set everytime a new card is created
    'updated_date automatically set everytime a card is updated
    'archived' is set to True when a user want to archive the card
    """

    board_list = models.ForeignKey('List', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    card_title = models.CharField(max_length=200)
    card_description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.card_title


class CardImage(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    empty = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.card.id}'


class List(models.Model):
    """
    'board' is the board the list is member of
    'author' is the user who created the list
    'list_title' is the title of the list
    'created_date' automatically set everytime a new list is created
    'updated_date automatically set everytime a list is updated
    'archived' is set to True when a user want to archive the list
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    list_title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.list_title


class Board(models.Model):
    """
    'author' is the user who created the board
    Automatically assign value to 'created_date' when instance is created.
    Automatically update value to 'updated_date' when save method is called.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, editable=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BoardMembers(models.Model):
    """
    'board' is the board.
    'members' are the member of the board
    'deactivate' status of the member is equal to False when member is being added to the board.
    'owner' is the user who created the board.
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    members = models.ForeignKey(User, on_delete=models.CASCADE)
    deactivate = models.BooleanField(default=True)
    owner = models.BooleanField(default=False)


class BoardInvite(models.Model):
    """
    Stores the inivited user with no existing account here.
    """

    board_member = models.ForeignKey('BoardMembers', on_delete=models.CASCADE)
    email_member = models.CharField(max_length=200)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime


class Card(models.Model):
    board_list = models.ForeignKey('List', on_delete=models.CASCADE)
    card_title = models.CharField(max_length=200)
    card_description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.card_title


class List(models.Model):
    """
    Dapat niya tawagon ang pangalan sa board member na naghimo sa list
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
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
    Kwaa ang board.
    Kwaa ang nagcreate sa board tapos ibutang kay members.
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    members = models.ForeignKey(User, on_delete=models.CASCADE) #author sa board
    deactivate = models.BooleanField(default=True)
    owner = models.BooleanField(default=False)

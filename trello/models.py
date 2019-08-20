from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from datetime import datetime


class List(models.Model):
    """
    Dapat niya tawagon ang pangalan sa board member na naghimo sa list
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE) #one to many queryset view
    boardmember = models.ForeignKey('BoardMembers', on_delete=models.CASCADE)
    list_title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.list_title


class Board(models.Model):
    """
    'author' is the user who created the board
    Automatically assign value to 'created_date' when instance is created.
    Automatically update value to 'updated_date' when save method is called.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #boardmember na instance, iassign ang value ani gamit ang queryset. 
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.title


class BoardMembers(models.Model):
    """
    Create board members to the specific board, with its members, and their ownership status.
    If member is the board author, then owner is equals to True.
    """

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    members = models.CharField(max_length=200) #author sa board
    deactivate = models.BooleanField(default=True)
    owner = models.BooleanField(default=False)

    
    






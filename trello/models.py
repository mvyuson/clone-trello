from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    card_title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.card_title

    def update(self):
        self.update_date = timezone.now()
        self.save()


class List(models.Model):
    card_id = models.ForeignKey(Card, null=True, default=None, on_delete=models.CASCADE)
    list_title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.list_title

    def update(self):
        self.updated_date = timezone.now()
        self.save()


class Board(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.CASCADE)
    list_id = models.ForeignKey(List, null=True, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def update(self):
        self.updated_date = timezone.now()
        self.save()


class BoardMembers(models.Model):
    board_id = models.ForeignKey(Board, null=True, default=None, on_delete=models.CASCADE)




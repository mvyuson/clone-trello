from django.contrib import admin
from django.contrib.auth.models import User
from .models import List, Board, BoardMembers, Card, BoardInvite, CardImage

admin.site.register(List)
admin.site.register(Board)
admin.site.register(BoardMembers)
admin.site.register(Card)
admin.site.register(BoardInvite)
admin.site.register(CardImage)
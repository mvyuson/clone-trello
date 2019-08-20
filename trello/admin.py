from django.contrib import admin
from django.contrib.auth.models import User
from .models import List, Board, BoardMembers

admin.site.register(List)
admin.site.register(Board)
admin.site.register(BoardMembers)
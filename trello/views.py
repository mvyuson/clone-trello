from django.views.generic import TemplateView, RedirectView
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .forms import (
    SignupForm, 
    LoginForm, 
    AddBoardTitleForm, 
    AddListForm
)
from .models import List, Board

import json


class SignupView(TemplateView):
    form = SignupForm
    template_name = 'trello/signup.html'

    def get(self, *args, **kwargs):
        form = SignupForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        #import pdb; pdb.set_trace()
        if form.is_valid():
            myuser = form.save()
            myuser.save()
            return redirect('login')
        context = {'form':form}
        return render(self.request, self.template_name, context)



class LoginView(TemplateView):
    form = LoginForm
    template_name = 'trello/login.html'
    
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        context = {'form':form}
        if form.is_valid():
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                login(self.request, user)
                return redirect('dashboard') 
            else:
                print("Check username and password")
                return render(self.request, self.template_name, context)
        return render(self.request, self.template_name, context)


class LogoutView(RedirectView):
    """
    Logout User
    """

    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')


class DashBoardView(LoginRequiredMixin, TemplateView):
    """
    Redirect to Login page when user logout.
    """
    login_url = '/login/'
    template_name = 'trello/list.html'
    form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        board = Board.objects.filter(author=self.request.user).order_by('id')
        return render(self.request, self.template_name, {'board':board})
 

class CreateBoardView(TemplateView):
    """
    Redirect to board with the saved board title.
    Dapat iinclude niya ang whitespace
    """

    template_name = 'trello/create-board.html' 
    form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name,  {'form':form})

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        form = self.form(self.request.POST)
        """
        Undefine board_id
        """
        if form.is_valid():
            board = form.save(commit=False)
            board.author = self.request.user
            board.save()
            print(board.id)
            return JsonResponse({'board':board.id})
        return render(self.request, self.template_name,  {'form':form})
 

class BoardView(TemplateView):
    """
    Display the current board title by calling its id

    Get the current Board
    """

    template_name = 'trello/board.html'

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("id"))
        context = {'board':board.id}
        return render(self.request, self.template_name, context)


class ListView(TemplateView):
    template_name = 'trello/board.html'

    def get(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        #current_list = get_object_or_404(List, list_title=kwargs.get("list_title"))
        #current_list = List.objects.filter(list_title='list_title').last()
        current_list = List.objects.latest('list_title')
        print(current_list)
        return render(self.request, self.template_name, {'current_list':current_list})

class BoardListView(TemplateView):
    template_name = 'trello/base.html'

    def post(self, *args, **kwargs):
        all_boards = Board.objects.all(title='title')
        context = {'all_boards':all_boards}
        return render(self.request, self.template_name, context)


class UpdateListView(TemplateView):
    template_name = 'trello/create-list.html'

    def get(self, *args, **kwargs):
        post = get_object_or_404(List, pk=kwargs.get("pk"))
        form = AddListForm(instance=post)
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        post = get_object_or_404(List, pk=kwargs.get("pk"))
        form = AddListForm(self.request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            current_board = get_object_or_404(Board, title=kwargs.get("title"))
            post.board = current_board
            post.save()

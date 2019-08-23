from django.views.generic import TemplateView, RedirectView, View
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .forms import (
    SignUpForm, 
    LoginForm, 
    AddBoardTitleForm, 
    AddListForm
)
from .models import List, Board

import json


class SignUpView(TemplateView):
    """
    View for the signup.
    """

    form = SignUpForm
    template_name = 'trello/signup.html'

    """
    Render form to signup page.
    """

    def get(self, *args, **kwargs):
        form = SignUpForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)

    """
    If form is validated, the user will be redirected to login page.
    If not, form will be rerendered.
    """

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            myuser = form.save()
            return redirect('login')
        context = {'form':form}
        return render(self.request, self.template_name, context)


class LoginView(TemplateView):
    """
    View for login.
    """
    
    form = LoginForm
    template_name = 'trello/login.html'
    #import pdb; pdb.set_trace()

    """
    Render login form to login page.
    """
    
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)

    """
    Assign username and password with the values retrieved from form.
    If form is valid after validating, django will authenticate user
    by comparing the data entered vs data registered in the database.
    If user credentials have a matching values from the database, the 
    user will turn as active and will be redirected to the dashboard.
    Else the method will rerender the form.
    """

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
    Display all the boards made by the user.
    Render Add Board form.
    """
    
    login_url = '/login/'
    template_name = 'trello/list.html'
    form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        board = Board.objects.filter(author=self.request.user).order_by('id')
        return render(self.request, self.template_name, {'board':board})
 

class CreateBoardView(TemplateView):
    """
    When 'Create Board' is clicked, add board form will render.
    Redirect to board with the saved board title.
    """

    template_name = 'trello/create-board.html' 
    form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name,  {'form':form})

    """
    If form is valid, form.save(commit=False). 
    It indicates that don't save the form yet
    because the author of the board which
    is the current user of the page was 
    have not been set yet.
    After the board author has been assigned,
    the form will be save.
    Then return a JsonResponse with board as
    argument.

    If form is not valid, this view will return
    an error 400 which indicates that the server
    can't process sent by the user may be due to 
    invalid syntax or attempting on submitting the
    form with empty values.
    """

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = self.request.user
            board.save()
            return JsonResponse({'board':board.id})    
        else:
            return HttpResponse(status=400)
        return render(self.request, self.template_name,  {'form':form})
 

class BoardView(TemplateView):
    """
    Display the current board title by calling its id

    Get the current Board
    """

    template_name = 'trello/board.html'
    form = AddListForm

    def get(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        board = get_object_or_404(Board, id=kwargs.get("id"))
        form = self.form()
        #board = board.id
        context = {'board':board, 'form':form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            board_list = form.save(commit=False)
            board_list.board = get_object_or_404(Board, id=kwargs.get("id"))
            board = board_list.board
            board_list.save()
            board_list = List.objects.filter(board=board).order_by('id') 
            form = AddListForm()
            context = {'board':board, 'board_list':board_list, 'form':form}
            #return render(self.request, self.template_name, context)
            return redirect('board', id=board.id)
        return render(self.request, self.template_name, {'form':form})
        

class ListView(TemplateView):
    template_name = 'trello/create-list.html'
    form = AddListForm

    def get(self, *args, **kwargs):
        board_list = List.objects.order_by("id")
        context = {'board_list':board_list}
        print(board_list)
        return render(self.request, self.template_name, context)


class UpdateBoard(View):
    def post(self, *args, **kwargs):
        data = dict()
        board = Board.objects.get(id=id)
        """
        contenteditable ang frontend. pero dapat ka maghimo og forms
        """

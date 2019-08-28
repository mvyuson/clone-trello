from django.views.generic.edit import DeleteView
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
    AddListForm, 
    AddCardForm,
    AddCardDescriptionForm,
)
from .models import Card, List, Board

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
            form.save()
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
    If form is valid, form.save(commit=False). It indicates that don't 
    save the form yet because the author of the board which is the current 
    user of the page was have not been set yet. After the board author has 
    been assigned, the form will be save. Then return a JsonResponse with 
    board as argument.

    If form is not valid, this view will return an error 400 which indicates 
    that the server can't process sent by the user may be due to invalid syntax 
    or attempting on submitting the form with empty values.
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
    card_form = AddCardForm

    def get(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        """
        Get the kwargs of board_list
        """

        board = get_object_or_404(Board, id=kwargs.get("id"))        
        form = self.form()
        card_form = self.card_form()
        context = {'board':board, 'form':form, 'card_form':card_form}
        return render(self.request, self.template_name, context)    

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            board_list = form.save(commit=False)
            board_list.board = get_object_or_404(Board, id=kwargs.get('id'))
            board_list.save()
            return redirect('board', board_list.board.id)
        return render(self.request, self.template_name, {'form':form, })


class AddCardView(TemplateView):
    template_name = 'trello/board.html'
    form = AddCardForm

    def post(self, request, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            board_list = get_object_or_404(List, id=kwargs.get('id'))
            card.board_list = board_list
            card.save()
            print(card.card_title, "CARD")
            return redirect('board', board_list.board.id)
        return render(self.request, self.template_name, {'form':form})


class UpdateBoard(TemplateView):
    template_name = 'trello/edit.html'
    
    def get(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        edit_board = get_object_or_404(Board, id=kwargs.get('id'))
        form = AddBoardTitleForm(instance=edit_board)
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        edit_board = get_object_or_404(Board, id=kwargs.get('id'))
        form = AddBoardTitleForm(self.request.POST, instance=edit_board)
        if form.is_valid():
            edit_board = form.save(commit=False)
            edit_board.author = self.request.user
            edit_board.save()
            return redirect('board', id=edit_board.id)
        return render(self.request, self.template_name, {'form':form})


class DeleteBoardView(DeleteView):
    def get(self, *args, **kwargs):
        board_to_delete = get_object_or_404(Board, id=kwargs.get('id'))
        board_to_delete.delete()
        return redirect('dashboard')

class UpdateListView(TemplateView):
    template_name = 'trello/edit.html'

    def get(self, *args, **kwargs):
        edit_list = get_object_or_404(List, id=kwargs.get('id'))
        form = AddListForm(instance=edit_list)
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        edit_list = get_object_or_404(List, id=kwargs.get('id'))
        form = AddListForm(self.request.POST, instance=edit_list)
        if form.is_valid():
            edit_list = form.save()
            return redirect('board', id=edit_list.board.id)
        return render(self.request, self.template_name, {'form':form})


class DeleteListView(DeleteView):
    def get(self, *args, **kwargs):
        list_to_delete = get_object_or_404(List, id=kwargs.get('id'))
        board = list_to_delete.board.id
        list_to_delete.delete()
        return redirect('board', board)


class CardDescriptionView(TemplateView):
    template_name = 'trello/description.html'
    form = AddCardDescriptionForm

    def get(self, *args, **kwargs):
        card_description = get_object_or_404(Card, id=kwargs.get('id'))
        form = self.form()
        context = {'card_description':card_description, 'board_list':card_description.board_list.id, 'form':form}
        return render(self.request, self.template_name, context)


class ArchiveView(TemplateView):
    template_name = 'trello/board_archive.html'

    def get(self, *args, **kwargs):
        #boards = Board.objects.filter(user=self.request.author, board__archived=False, is_confirmed=True).order_by('id')
        board = Board.objects.filter(author=self.request.user)
        context = {'board':board}
        return render(self.request, self.template_name, context)

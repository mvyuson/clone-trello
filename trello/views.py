from django.views.generic.edit import DeleteView, UpdateView
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
from django.contrib.auth.models import User

from .forms import (
    SignUpForm, 
    LoginForm, 
    AddBoardTitleForm, 
    AddListForm, 
    AddCardForm,
    AddCardDescriptionForm,
    InviteMemberForm,
)
from .models import Card, List, Board, BoardMembers

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
        board = Board.objects.filter(author=self.request.user, archived=False).order_by('id')
        board_member = BoardMembers.objects.filter(members=self.request.user).order_by('id')
        board_owner = BoardMembers.objects.filter(owner=True)
        return render(self.request, self.template_name, {'board':board, 'board_member':board_member, 'board_owner':board_owner})
 

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
    board_form = AddBoardTitleForm
    invite_form = InviteMemberForm

    def get(self, *args, **kwargs):
        """
        Get the kwargs of board_list
        """
        #import pdb; pdb.set_trace()

        board = get_object_or_404(Board, id=kwargs.get("id")) 
        board_members = BoardMembers.objects.filter(board=board).order_by('id')
        form = self.form()
        card_form = self.card_form()
        invite_form = self.invite_form()
        board_form = self.board_form(self.request.POST, instance=board)
        context = {'board':board, 'board_members':board_members, 'form':form, 'card_form':card_form, 'board_form':board_form, 'invite_form':invite_form,}
        return render(self.request, self.template_name, context)    

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            board_list = form.save(commit=False)
            board_list.board = get_object_or_404(Board, id=kwargs.get('id'))
            board_list.author = self.request.user
            board_list.save()
            return JsonResponse({'board_list':board_list.list_title, 'id':board_list.id})
        else: 
            return HttpResponse(status=400)
        return render(self.request, self.template_name, {'form':form})


class AddCardView(TemplateView):
    template_name = 'trello/board.html'
    form = AddCardForm

    def post(self, request, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            board_list = get_object_or_404(List, id=kwargs.get('id'))
            card.board_list = board_list
            card.author = self.request.user
            card.save()
            print(card.card_title, "CARD")
            return redirect('board', board_list.board.id)
        return render(self.request, self.template_name, {'form':form})


class CardDescriptionView(TemplateView):
    template_name = 'trello/description.html'
    form = AddCardDescriptionForm
    card_form = AddCardForm

    def get(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id'))
        card_form = self.card_form(self.request.POST, instance=card)
        form = self.form(self.request.POST, instance=card)
        context = {'card':card, 'board_list':card.board_list.id, 'form':form, 'card_form':card_form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        card = get_object_or_404(Card, id=kwargs.get('id'))
        card_form = self.card_form(self.request.POST, instance=card)
        if card_form.is_valid():
            card_form.save()
            board = card.board_list.board.id 
            print(board)
            return redirect('board', card.board_list.board.id)
        return render(self.request, self.template_name, {'card_form':card_form})


class AddCardDescriptionView(TemplateView):
    template_name = 'trello/description.html'
    form = AddCardDescriptionForm

    """
    Wala nisulod dire
    """

    def post(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        card = get_object_or_404(Card, id=kwargs.get('id'))
        form = self.form(self.request.POST, instance=card)
        if form.is_valid():
            card_description = form.save()
            card_description.author = self.request.user
            print(card_description, "KOKOKOKOK")
            return redirect('board', card.board_list.board.id)
        return render(self.request, self.template_name, {'form':form})


class UpdateBoard(TemplateView):
    def post(self, *args, **kwargs):
        update_board = self.request.POST.get('board_title') 
        board = get_object_or_404(Board, id=kwargs.get('id'))
        current_board = Board.objects.get(id=board.id)
        current_board.title = update_board 
        current_board.save()
        return JsonResponse({'board':current_board.title})


class UpdateListView(TemplateView):
    def post(self, *args, **kwargs):
        update_list = self.request.POST.get('list_title')
        print(update_list)
        board_list = get_object_or_404(List, id=kwargs.get('id')) #mali
        current_list = List.objects.get(id=board_list.id)
        current_list.list_title = update_list
        current_list.save()
        print(current_list.list_title, 'KOKOKOKO')
        return JsonResponse({'board_list':current_list.list_title})


class DeleteBoardView(DeleteView):
    def get(self, *args, **kwargs):
        board_to_delete = get_object_or_404(Board, id=kwargs.get('id'))
        board_to_delete.delete()
        return redirect('dashboard')


class DeleteListView(DeleteView):
    def get(self, *args, **kwargs):
        list_to_delete = get_object_or_404(List, id=kwargs.get('id'))
        board = list_to_delete.board.id
        list_to_delete.delete()
        return redirect('board', board)


class DeleteCardView(DeleteView):
    def get(self, *args, **kwargs):
        card_to_delete = get_object_or_404(Card, id=kwargs.get('id'))
        board = card_to_delete.board_list.board.id 
        card_to_delete.delete()
        return redirect('board', board)


class BoardArchiveView(View):
    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        board.archived = True 
        board.save()
        return redirect('dashboard')


class ListArchiveView(View):
    def get(self, *args, **kwargs):
        board_list = get_object_or_404(List, id=kwargs.get('id'))
        board_list.archived = True 
        board_list.save()
        return JsonResponse({'board':board_list.board.id})


class CardArchiveView(View):
    def get(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id'))
        card.archived = True 
        card.save()
        return redirect('board', card.board_list.board.id)


class ArchiveView(TemplateView):
    template_name = 'trello/board_archive.html'

    def get(self, *args, **kwargs):
        archive_boards = Board.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        archive_list = List.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        archive_card = Card.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        context = {'archive_boards':archive_boards, 'archive_list':archive_list, 'archive_card':archive_card}
        return render(self.request, self.template_name, context)


class InviteMemberView(TemplateView):
    template_name = 'trello/board.html'
    form = InviteMemberForm

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        form = self.form(self.request.POST)
        board = get_object_or_404(Board, id=kwargs.get('id'))
        new_member = self.request.POST.get('members')
        if form.is_valid():                                            
            member = form.save(commit=False)
            member.board = get_object_or_404(Board, id=kwargs.get('id'))
            member.deactivate = False
            member.owner = True
            member.save()
            return redirect('board', board.id)
        return render(self.request, self.template_name, {'form':form})  

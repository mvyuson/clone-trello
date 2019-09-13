from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import TemplateView, RedirectView, View
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings


from .forms import (
    SignUpForm, 
    LoginForm, 
    AddBoardTitleForm, 
    AddListForm, 
    CardImageForm,
    UserProfileForm,
    EditUserForm
)

from .models import (
    Card, 
    List, 
    Board, 
    BoardMembers, 
    BoardInvite, 
    CardImage, 
    UserProfile
)

import json


"""
REMINDER: THE APP MUST NOT ACCEPT AND RETURN BLANK VALUES WHEN UPDATING.
          UPDATE CARD AND CREATE CARD DESCRIPTION MUST HAVE THE SAME VIEW
          FUNCTION.
"""

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
        card_image = CardImage.objects.all()
        board_owner = BoardMembers.objects.filter(owner=True)
        return render(self.request, self.template_name, {'board':board, 'board_member':board_member, 'board_owner':board_owner, 'card_image':card_image})
 

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
            create_board_member = BoardMembers.objects.create(board=board, members=self.request.user, deactivate=False, owner=True)
            create_board_member.save()
            return JsonResponse({'board':board.id})    
        else:
            return HttpResponse(status=400)
        return render(self.request, self.template_name,  {'form':form})


class BoardView(TemplateView):
    """
    Display the board details by returning the board, board_members, and other forms to the template.
    Get the current Board and save the newly added list
    """

    template_name = 'trello/board.html'
    form = AddListForm
    board_form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        """
        Get the kwargs of board_list
        """

        if self.request.POST.get('card_title'):
            card_list = get_object_or_404(List, id=kwargs.get('id'))
            title = self.request.POST.get('card_title')
            card = Card.objects.create(card_title=title, board_list=card_list, author=self.request.user)
            return JsonResponse({'card':card.card_title, 'id':card.id})

        board = get_object_or_404(Board, id=kwargs.get("id")) 
        board_members = BoardMembers.objects.filter(board=board).order_by('id')
        form = self.form()
        board_form = self.board_form(self.request.POST, instance=board)
        card_image = CardImage.objects.all().first()
        context = {'board':board, 'board_members':board_members, 'form':form, 'board_form':board_form, 'card_image':card_image}
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
    """
    Add a newly created card.
    """

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('card_title'):
            card_list = get_object_or_404(List, id=kwargs.get('id'))
            title = self.request.POST.get('card_title')
            card = Card.objects.create(card_title=title, board_list=card_list, author=self.request.user)
            card.save()
            return JsonResponse({'card':card.card_title, 'id':card.id})


class CardDescriptionView(TemplateView):
    """
    Display the card detail of a card inside the modal.
    """

    template_name = 'trello/description.html'
    form = CardImageForm

    def get(self, *args, **kwargs):
        form = self.form()
        card = get_object_or_404(Card, id=kwargs.get('id'))
        #import pdb; pdb.set_trace()
        card_image = CardImage.objects.filter(card=card)
        print(card_image)
        #card_image = CardImage.objects.all()
        context = {'card':card, 'board_list':card.board_list.id, 'card_image':card_image, 'form':form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id')) 
        update_card = self.request.POST.get('card_title') 
        update_description = self.request.POST.get('card_description') 
        
        current_card = Card.objects.get(id=card.id)
        current_description = Card.objects.get(id=card.id)
        proxy_description = current_description.card_description

        if update_card is None:
            current_card.card = card 
        else:
            current_card.card_title = update_card
        
        if update_description is None:
            current_card.card_description = current_description.card_description
        else:
            current_card.card_description = update_description

        print(current_card.card_title)
        current_card.save()
        return JsonResponse({'card':current_card.card_title, 'id':current_card.id, 'card_description': current_card.card_description, 'board': current_card.board_list.board.id})



class CardDragAndDropView(View):
    """
    Drag and drop card to a list and update it's list.
    1. Get the value of the dragged and dropped card, and the value of 
       the list it was dropped.
    2. Set the new list value of card with the value of the list it was
       dropped.
    3. Save.
    """

    def post (self, *args, **kwargs):
        drop_list = self.request.POST.get('blist')
        card = self.request.POST.get('card')
        drop_card = get_object_or_404(Card, id=kwargs.get('id'))
        current_card = Card.objects.get(id=card)
        current_list = List.objects.get(id=drop_list)
        current_card.board_list = current_list
        current_card.save()
        return JsonResponse({'card':current_card.id})


class UpdateBoard(TemplateView):
    """
    Update the value of the board title.
    1. Get the new value of the current board.
    2. Update the new value of the current board
    """

    def post(self, *args, **kwargs):
        update_board = self.request.POST.get('board_title') 
        board = get_object_or_404(Board, id=kwargs.get('id'))
        current_board = Board.objects.get(id=board.id)
        current_board.title = update_board 
        current_board.save()
        return JsonResponse({'board':current_board.title})


class UpdateListView(TemplateView):
    """
    Update the value of the list title.
    1. Get the new list value from the frontend.
    2. Get the id of the edited list.
    3. Get the id passed by the url
    4. Update List and save.
    """

    def post(self, *args, **kwargs):
        edit_list = self.request.POST.get('list_data')     
        list_id = self.request.POST.get('list_id')      
        current_list = get_object_or_404(List, id=kwargs.get('id')) 
        update_list = List.objects.get(id=list_id)
        update_list.list_title = edit_list
        print(update_list.list_title)
        update_list.save()
        return JsonResponse({'board_list':update_list.id})


class DeleteBoardView(DeleteView):
    """
    Delete the current Board.
    """
    
    def get(self, *args, **kwargs):
        board_to_delete = get_object_or_404(Board, id=kwargs.get('id'))
        board_to_delete.delete()
        return redirect('dashboard')


class DeleteListView(DeleteView):
    """
    Delete the current List.
    """
    
    def get(self, *args, **kwargs):
        list_to_delete = get_object_or_404(List, id=kwargs.get('id'))
        board = list_to_delete.board.id
        list_to_delete.delete()
        return redirect('board', board)


class DeleteCardView(DeleteView):
    """
    Delete the current Card.
    """

    def get(self, *args, **kwargs):
        card_to_delete = get_object_or_404(Card, id=kwargs.get('id'))
        board = card_to_delete.board_list.board.id 
        card_to_delete.delete()
        return redirect('board', board)


class BoardArchiveView(View):
    """
    Archive Board by setting its archived field into True.
    """

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        board.archived = True 
        board.save()
        return JsonResponse({'board':board.id})


class RestoreArchivedBoard(View):
    """
    Restore Archived Board
    """

    def get(self, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get('id'))
        board.archived = False 
        board.save()
        return redirect('dashboard')


class RestoreArchivedList(View):
    """
    Restore Archived List
    """

    def get(self, *args, **kwargs):
        board_list = get_object_or_404(List, id=kwargs.get('id'))
        board_list.archived = False
        board_list.save()
        return redirect('board', board_list.board.id)


class RestoreArchivedCard(View):
    """
    Restore Archived Card
    """

    def get(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id'))
        card.archived = False 
        card.save()
        return redirect('board', card.board_list.board.id)


class ListArchiveView(View):
    """
    Archive List by setting its archived field into True.
    """

    def get(self, *args, **kwargs):
        board_list = get_object_or_404(List, id=kwargs.get('id'))
        board_list.archived = True 
        board_list.save()
        return JsonResponse({'board':board_list.board.id})


class CardArchiveView(View):
    """
    Archive Card by setting its archived field into True.
    """

    def get(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id'))
        card.archived = True 
        card.save()
        return JsonResponse({'board':card.board_list.board.id})


class ArchiveView(TemplateView):
    """
    Display the archive boards, lists, and cards in one template order by the date it was created.
    1. Get all the boards with the current user as the author, and if archived is equal to true, order
       by the date it was created.
    2. Get all the lists with the current user as the author, and if archived is equal to true, order
       by the date it was created.
    3. Get all the cards with the current user as the author, and if archived is equal to true, order
       by the date it was created.
    """

    template_name = 'trello/board_archive.html'

    def get(self, *args, **kwargs):
        archive_boards = Board.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        archive_list = List.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        archive_card = Card.objects.filter(author=self.request.user, archived=True).order_by('created_date')
        context = {'archive_boards':archive_boards, 'archive_list':archive_list, 'archive_card':archive_card}
        return render(self.request, self.template_name, context)


class InviteMemberView(TemplateView):
    """
    Invite other user as a member of the board. The user will enter the username of the member
    and submit it. Then activate its membership. Then set the current user as the owner of the 
    board. Then redirect it to Board Details.

    REMINDER: Convert it into AJAX 
    """

    template_name = 'trello/board.html'

    def send_email_msg(self, message, to_email):
        send_mail(
            'Invite Member',
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
        )

    def post(self, *args, **kwargs):
        member_email = self.request.POST.get('member_email')
        board = get_object_or_404(Board, id=kwargs.get('id'))
        try:
            member = User.objects.get(email=member_email)
            message = 'You are invited by {} to join board {}. Click the link below to join. http://192.168.2.216:8000//dashboard'.format(self.request.user.username, board.title)
            self.send_email_msg(message, member_email)

            current_member = User.objects.get(email=member_email)
            new_board_member = BoardMembers.objects.create(board=board, members=current_member, deactivate=False, owner=False)
            new_board_member.save()
            return redirect('board', board.id)
        except User.DoesNotExist():
            message = 'You are invited by {} to join board {}. Click the link below to join. http://192.168.2.216:8000//register'.format(invite_by, board.title)
            self.send_email_msg(message, member_email)
            initial_member = BoardInvite.objects.create(board=board, email_member=member_email)
            return redirect('board', board.id)


class RegisterInvitedUser(View):
    form = SignUpForm
    template_name = "trello/register_invited_user.html"

    def get(self, *args, **kwargs):
        form = self.form()
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        form = self.form(self.request.POST)
        if form.is_valid():
            user = form.save()
            #invite = BoardInvite.objects.get(code=kwargs.get('code'))
            # invite = BoardInvite.objects.filter(email_member=member_email)
            new_member = BoardInvite.objects.get(email_member=invite.email)
            new_board_member = BoardMembers.objects.create(board=invite.board, members=user, deactivate=False)
            return redirect('login')
        return HttpResponse(status=400)

        

class LeaveBoardView(View):
    """
    Let the user who is a member of the board to leave by setting the deactivating its membership.
    """

    def get(self, *args, **kwargs):
        print(self.request.user)
        board = get_object_or_404(Board, id=kwargs.get('id'))
        board_member = BoardMembers.objects.get(board=board, members=self.request.user)
        board_member.deactivate = True
        board_member.save()
        return redirect('dashboard')


class EditUserProfile(TemplateView):
    template_name = 'trello/user_profile.html'

    def get(self, *args, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        print(user)
        context = {'userprofile':user}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        update_username = self.request.POST.get('profile_username')
        update_email = self.request.POST.get('profile_email')
        update_bio = self.request.POST.get('profile_bio')
        user = User.objects.get(id=self.request.user.id)
        user.username = update_username
        user.email = update_email
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.bio = update_bio
        user_profile.save()
        print('User Edited')
        # return redirect('user-profile')
        return JsonResponse({'user':user.username})


class DeleteCardCoverImage(DeleteView):
    def get(self, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get('id'))
        CardImage.objects.filter(card=card).delete()
        return JsonResponse({'card':card.id})


class UploadImageView(View):
    template_name = 'trello/description.html'
    form = CardImageForm

    def post(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        form = self.form(self.request.POST, self.request.FILES)
        parent_card = get_object_or_404(Card, id=kwargs.get('id'))
        images = CardImage.objects.filter(card=parent_card)

        if images is None:
            pass 
        else:
            CardImage.objects.filter(card=parent_card).delete()
            
        if form.is_valid():
            card_image = form.save(commit=False)
            this_card = CardImage.objects.filter(card=parent_card)
            if this_card.exists():
                return redirect('board', parent_card.board_list.board.id)
            else:
                card_image.card = parent_card
                card_image.empty=True
                str_card_image = str(card_image.image)
                print(str_card_image)
                print(card_image.image.url)
                card_image.save()
                return redirect('board', parent_card.board_list.board.id)
        return HttpResponse(status=400)

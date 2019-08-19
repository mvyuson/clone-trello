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
from .models import Board

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
    template_name = 'trello/dashboard.html'
    form = AddBoardTitleForm

    def get(self, *args, **kwargs):
        form = AddBoardTitleForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        title = self.request.POST.get('title')
        context = {'form':form}
        if form.is_valid():
            title = form.save()
            return redirect('board', title=title)
        return render(self.request, self.template_name, context)


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
        form = self.form(self.request.POST)
        if form.is_valid():
            title = form.save()
            title.created_date = timezone.now()
            title.save()
            title = self.request.POST.get('title')
            return HttpResponse(json.dumps({'title':title}), content_type="application/json")
        return render(self.request, self.template_name,  {'form':form})
 

class BoardView(RedirectView):
    """
    Display the current board title by calling its id
    """

    template_name = 'trello/board.html'
    form = AddListForm

    def get(self, *args, **kwargs):
        current_board = get_object_or_404(Board, title=kwargs.get("title"))
        title = current_board.title
        form = self.form()
        return render(self.request, self.template_name, {'title':title, 'form':form})

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        current_board = get_object_or_404(Board, title=kwargs.get("title"))
        title = current_board.title
        if form.is_valid():
            list_title = form.save()
            form = self.form()
        return render(self.request, self.template_name, {'title':title, 'form':form})


class CreateListView(TemplateView):
    template_name = 'trello/board.html'
    

    def get(self, *args, **kwargs):
        form = self.form()
        return redirect(self.request.META['HTTP_REFERER'], {'form':form})

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            list_title = form.save()
            
            
        return render(self.request, self.template_name, {'form':form})


class PasswordResetView(TemplateView):
    def get(self, *args, **kwargs):
        email = self.request.POST.get('email')
        send_mail(
            'Reset Password',
            'Reset Password',
            'webmaster@localhost',
            email,
            html_content = render_to_string('registration/password_reset_email.html')
        )


    
    
        
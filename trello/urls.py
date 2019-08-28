from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.generic.dates import ArchiveIndexView
from trello.views import (
        SignUpView, 
        LoginView,
        DashBoardView,
        LogoutView,
        BoardView,
        CreateBoardView,
        AddCardView,
        UpdateBoard,
        DeleteBoardView,
        UpdateListView,
        DeleteListView,
        CardDescriptionView,
        ArchiveView,
)
from .models import Board
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset_done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('board/<int:id>/', BoardView.as_view(), name='board'),
    path('board/<int:id>/list/', AddCardView.as_view(), name='add_card'),
    path('board/<int:id>/edit-board/', UpdateBoard.as_view(), name='edit-board'),
    path('board/<int:id>/delete-board/', DeleteBoardView.as_view(), name='delete-board'),
    path('board/<int:id>/edit-list/', UpdateListView.as_view(), name='edit-list'),
    path('delete-list/<int:id>', DeleteListView.as_view(), name='delete-list'),
    #path('board_archive/', ArchiveIndexView.as_view(model=Board, date_field="created_date")),
    path('board_archive/', ArchiveView.as_view(), name='board_archive'),
    path('description/<int:id>', CardDescriptionView.as_view(), name='description'),
]
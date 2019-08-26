from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from trello.views import (
        SignUpView, 
        LoginView,
        DashBoardView,
        LogoutView,
        BoardView,
        CreateBoardView,
        AddCardView,
        ListView,
        UpdateBoard,
)

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
    path('create-board/', CreateBoardView.as_view(), name='board-create'),
    path('board/<int:id>/', BoardView.as_view(), name='board'),
    path('board/<int:id>/list', AddCardView.as_view(), name='add_card'),
    path('board/<int:id>/edit', UpdateBoard.as_view(), name='update-board'),
    #path('create-list/', ListView.as_view(), name='create-list')
]
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # User views
    path('users/create/', views.create_user, name='create_user'),
    path('users/list/', views.list_users, name='list_users'),
    path('users/describe/', views.describe_user, name='describe_user'),
    path('users/update/', views.update_user, name='update_user'),
    path('users/teams/', views.get_user_teams, name='get_user_teams'),
    path('users/delete/', views.delete_user, name='delete_user'),
    
    # Team views
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/list/', views.list_teams, name='list_teams'),
    path('teams/describe/', views.describe_team, name='describe_team'),
    path('teams/update/', views.update_team, name='update_team'),
    path('teams/users/add/', views.add_users_to_team, name='add_users_to_team'),
    path('teams/users/remove/', views.remove_users_from_team, name='remove_users_from_team'),
    path('teams/users/list/', views.list_team_users, name='list_team_users'),
    path('teams/delete/', views.delete_team, name='delete_team'),
    
    # Board views
    path('boards/', views.list_boards, name='list_boards'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/close/', views.close_board, name='close_board'),
    path('boards/delete/', views.delete_board, name='delete_board'),
    path('boards/tasks/add/', views.add_task, name='add_task'),
    path('boards/tasks/update/', views.update_task_status, name='update_task_status'),
    path('boards/tasks/list/', views.list_board_tasks, name='list_board_tasks'),
    path('boards/export/', views.export_board, name='export_board'),
] 
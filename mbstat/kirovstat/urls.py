
from django.urls import path,re_path

from . import views
from .models import teams

app_name = 'kirovstat'
urlpatterns = [
    path('', views.index, name = 'index'),  
    # path('team_info/<int:team_id>/', views.team_info,  name = 'team_info'),
    re_path(r'^team_info/', views.team_info,  name = 'team_info'),
    re_path(r'^game_info/', views.game_info,  name = 'game_info'),
    re_path(r'^game_info/', views.game_info,  name = 'game_info'),
    
]

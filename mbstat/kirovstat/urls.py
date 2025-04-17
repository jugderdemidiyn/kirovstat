
from django.urls import path,re_path

from . import views
from . import views2
from .models import teams

app_name = 'kirovstat'
urlpatterns = [
    path('', views.index, name = 'index'),  
    # path('team_info/<int:team_id>/', views.team_info,  name = 'team_info'),
    re_path(r'^team_info/', views.team_info,  name = 'team_info'),
    re_path(r'^game_info/', views.game_info,  name = 'game_info'),
    #re_path(r'^statistic/', views.game_info,  name = 'stats'),
    re_path(r'^load_game/', views2.add_game,  name = 'load_game'),
    re_path(r'^year_stat/', views.year_stat,  name = 'year_stat'),
    re_path(r'^statstat/', views2.add_res_to_stat,  name = 'statstat'),
    re_path(r'^test1/', views2.test1,  name = 'test1'),
    
]

from . models import game_type, games, teams, gmdata
from datetime import date


#Получение все aka_id для команды

def get_akas (t_id):
    
    t_names = teams.objects.filter(t_aka=t_id)
    akas_list=[]
    for t in t_names:
        akas_list.append (t.id)

    return (akas_list)


# Получение данных по id команды (список с ака), начальная и конечная даты

def get_games_info (t_id_list , data_start = '2025-02-01', data_finish = '2025-02-28'):
    
    d1 = date.fromisoformat(data_start)
    d2 = date.fromisoformat(data_finish)
    
    games1  = games.objects.filter(g_date__gte=d1, g_date__lte=d2)   

    games_is_range=[]
    for t in games1:
        games_is_range.append (t.id)

    g_info = gmdata.objects.filter(gd_team__in=t_id_list, gd_game__in=games_is_range)    
    
    return (g_info)

def get_all_teams():
    
    t_names = teams.objects.all()

    return(t_names)
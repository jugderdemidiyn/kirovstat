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

def get_games_info (t_id_list , data_start = '2025-01-01', data_finish = '2025-12-31'):
    
    d1 = date.fromisoformat(data_start)
    d2 = date.fromisoformat(data_finish)
    
    games1  = games.objects.filter(g_date__gte=d1, g_date__lte=d2)   

    games_is_range=[]
    for t in games1:
        games_is_range.append (t.id)

    g_info = gmdata.objects.filter(gd_team__in=t_id_list, gd_game__in=games_is_range).order_by('gd_game')
    
    return (g_info)

def get_all_teams():
    
    t_names = teams.objects.all()

    return(t_names)



def get_teams_on_place (place , type1 = [1,2,3,4,5], data_start = '2025-01-01', data_finish = '2025-12-31'):

    d1 = date.fromisoformat(data_start)
    d2 = date.fromisoformat(data_finish)
    games1  = games.objects.filter(g_date__gte=d1, g_date__lte=d2) 
    
    games_is_range=[]
    for t in games1:
        games_is_range.append(t.id)
    
    
    g_info = gmdata.objects.filter(gd_place = place, gd_game__in=games_is_range) 
    
    set1 = set()
    for g in g_info:
      set1.add(g.gd_team_id)
    
    
    place_dict_all={}
    place_dict_class={}
    place_dict_tem={}
    place_dict_tuz={}
    place_dict_jub={}

    for i in game_type.objects.all():
        place_dict={}
        for s in set1:
            place_dict[s]=0
            for t in g_info:
                #print(t.gd_game.g_type_id, ' ', i.id) 
                
                if t.gd_team_id == s and t.gd_game.g_type_id == i.id:
                #    print(t.gd_game.g_type_id, ' in if ', i.id) 
                    place_dict[s] = place_dict[s]+1
                #print(place_dict)

    #return(place_dict)
    return(g_info)
from . models import game_type, games, teams, gmdata
from datetime import date
import collections as coll
from operator import itemgetter

#Получение игр по начальной и конечно дате
def get_games_all_in_range(d_s , d_f):

    d1 = date.fromisoformat(d_s)
    d2 = date.fromisoformat(d_f)
    games1  = games.objects.filter(g_date__gte=d1, g_date__lte=d2) 
    
    return(games1)

#Получение количества игр по начальной и конечно дате
def get_games_count(d_s , d_f):

    d1 = date.fromisoformat(d_s)
    d2 = date.fromisoformat(d_f)
    g_count  = games.objects.filter(g_date__gte=d1, g_date__lte=d2).count
    
    return(g_count)

#Получение списка игр по начальной и конечно дате
def get_games_in_range(d_s , d_f):

    d1 = date.fromisoformat(d_s)
    d2 = date.fromisoformat(d_f)
    games1  = games.objects.filter(g_date__gte=d1, g_date__lte=d2) 
    
    games_is_range=[]
    for t in games1:
        games_is_range.append(t.id)

    return(games_is_range)    

#Получение все aka_id для команды
def get_akas (t_id):
    
    t_names = teams.objects.filter(t_aka=t_id)
    akas_list=[]
    for t in t_names:
        akas_list.append (t.id)

    return (akas_list)


# Получение данных по id команды (список с ака), начальная и конечная даты

def get_games_info (t_id_list , data_start = '2025-01-01', data_finish = '2025-12-31'):
 

    g_r = get_games_in_range(data_start,data_finish)

    g_info = gmdata.objects.filter(gd_team__in=t_id_list, gd_game__in=g_r).order_by('gd_game')
    
    return (g_info)

def get_all_teams():
    
    t_names = teams.objects.all()

    return(t_names)


# получение словаря 
# по запросу места, списка типов игра и граничных дат
# возвращает словарь { id команды : [ количество мест, название команды ]}

def get_place (place , type1 = [1,2,3,4,5], data_start = '2025-01-01', data_finish = '2025-12-31'):

    game_r = get_games_in_range(data_start,data_finish)
    
    g_info = gmdata.objects.filter(gd_place = place, gd_game__in=game_r , gd_game__g_type__in=type1)
        
    results=[]
    for i in g_info:
        results.append(i.gd_team_id)

    c=coll.Counter(results)  
    c = dict(sorted(c.items(), key=itemgetter(-1), reverse = True))
    
    a={}
    d=[]
    
    for i in c.keys():
       d.append(c[i])
       d.append(teams.objects.values('t_name').get(pk=i)['t_name'])
       a[i]= d
       d=[] 
    
    return (a)
    


    
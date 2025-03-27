from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Sum
from . models import game_type, games, teams, gmdata
from . defs_1 import * 


def index(request): 
    g_count = games.objects.count()
    game1 = games.objects.all() 
    t_data = get_all_teams()     

    
    place_data_a_1=get_place(1,type1=[1,2,3,4,5]) 
    place_data_a_2=get_place(2,type1=[1,2,3,4,5]) 
    place_data_a_3=get_place(3,type1=[1,2,3,4,5]) 
    place_data_cl_1=get_place(1,type1=[1,5]) 
    place_data_cl_2=get_place(2,type1=[1,5]) 
    place_data_cl_3=get_place(3,type1=[1,5]) 
    place_data_tz_1=get_place(1,type1=[2]) 
    place_data_tz_2=get_place(2,type1=[2]) 
    place_data_tz_3=get_place(3,type1=[2])
    place_data_tem_1=get_place(1,type1=[3])  
    place_data_tem_2=get_place(2,type1=[3])  
    place_data_tem_3=get_place(3,type1=[3])  
     

    context = {'game1': game1, 'g_count' : g_count, 't_data' : t_data, \
               'place_data_a_1' : place_data_a_1, 'place_data_a_2' : place_data_a_2,'place_data_a_3' : place_data_a_3,\
               'place_data_cl_1' : place_data_cl_1, 'place_data_cl_2' : place_data_cl_2,'place_data_cl_3' : place_data_cl_3,\
               'place_data_tz_1' : place_data_tz_1, 'place_data_tz_2' : place_data_tz_2,'place_data_tz_3' : place_data_tz_3,\
               'place_data_tem_1' : place_data_tem_1, 'place_data_tem_2' : place_data_tem_2,'place_data_tem_3' : place_data_tem_3 }
 
    
    return render(request, 'game_list.html', context)   

    

def team_info (request):

    team_id = request.GET['team_id']
    # Основной ID команды
    main_id = teams.objects.values('t_aka_id').get(pk=team_id)['t_aka_id']
    # все названия команды
    t_names = teams.objects.filter(t_aka=main_id)
    t_foto = teams.objects.values('t_foto').get(pk=main_id)['t_foto']
    
    akas_list=get_akas(main_id)
    t_data_info = get_games_info (akas_list,'2025-01-01','2025-12-31')

    Max_place =t_data_info.aggregate(Min('gd_place')) ['gd_place__min']
    Min_place =t_data_info.aggregate(Max('gd_place')) ['gd_place__max']    
    g_count = len(t_data_info)
    
    l_p=      [0,0,0,0,0,0,0,0,0,0,0]
    l_p_class=[0,0,0,0,0,0,0,0,0,0,0]
    l_p_tuz=  [0,0,0,0,0,0,0,0,0,0,0]
    l_p_tem=  [0,0,0,0,0,0,0,0,0,0,0]
    l_p_jub=  [0,0,0,0,0,0,0,0,0,0,0]
    
    for t in t_data_info:   
      for i in range(1,11):
        if t.gd_place==i:
            l_p[i]=l_p[i]+1
            if t.gd_game.g_type_id==1 or t.gd_game.g_type_id==5:
               l_p_class[i]=l_p_class[i]+1
            elif t.gd_game.g_type_id==2:
               l_p_tuz[i]=l_p_tuz[i]+1
            elif t.gd_game.g_type_id==3:
               l_p_tem[i]=l_p_tem[i]+1
            else:
               l_p_jub[i]=l_p_jub[i]+1

    l=[1,2,3,4,5,6,7,8,9,10]
         

    context = {'t_data_info': t_data_info, 't_names': t_names, 't_foto': t_foto, 'Max_place': Max_place,'Min_place' :Min_place, 'g_count':g_count, 'l': l,'l_p' : l_p,'l_p_class' : l_p_class,'l_p_tuz' : l_p_tuz, 'l_p_tem' :l_p_tem,'l_p_jub':l_p_jub }
    
    return render(request, 'team_info.html', context)



def game_info (request):
    
    game_id = request.GET['game_id']
    g_data_info = gmdata.objects.filter(gd_game = game_id).order_by('gd_place')
    game_info =  games.objects.get(pk=game_id)
    a = games.objects.get(pk=game_id).g_sets
   
    tours=[]
    for i in range(1, a+1): 
       tours.append(i)

    if request.user.is_authenticated:
       change_yes=1
    else: change_yes=0

    
    context = {'g_data_info': g_data_info, 'game_info': game_info, 'tours' : tours, 'change_yes' : change_yes }
    
    return render (request, 'game_info.html', context )
    # return JsonResponse(context)
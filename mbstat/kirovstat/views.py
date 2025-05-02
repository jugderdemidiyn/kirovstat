from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Sum
from . models import game_type, games, teams, gmdata
from . defs_1 import * 
from . defs_2 import *
from . defs_3 import *


def index(request): 
    g_count = get_games_count('2025-01-01','2025-12-31')
    #game1 = games.objects.all() 
    game1 = get_games_all_in_range('2025-01-01','2025-12-31')
    t_data = get_all_teams()     
    year=2025 

    
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
    
    context = {
       #'rating_5_tuz': rating_5_tuz, 'rating_5_class': rating_5_class,'rating_5_summ': rating_5_summ,\
               'game1': game1, 'g_count' : g_count, 't_data' : t_data, 'year' : year, \
               'place_data_a_1' : place_data_a_1, 'place_data_a_2' : place_data_a_2,'place_data_a_3' : place_data_a_3,\
               'place_data_cl_1' : place_data_cl_1, 'place_data_cl_2' : place_data_cl_2,'place_data_cl_3' : place_data_cl_3,\
               'place_data_tz_1' : place_data_tz_1, 'place_data_tz_2' : place_data_tz_2,'place_data_tz_3' : place_data_tz_3,\
               'place_data_tem_1' : place_data_tem_1, 'place_data_tem_2' : place_data_tem_2,'place_data_tem_3' : place_data_tem_3 }
 
    
    return render(request, 'game_list.html', context)   

    

def team_info (request):

    test1 = request.GET
    team_id= test1['team_id']
    try:
       year = test1['year']
    except:
       year='2025'
    t_data = get_all_teams()
    # Основной ID команды
    main_id = teams.objects.values('t_aka_id').get(pk=team_id)['t_aka_id']
    # все названия команды
    t_names = teams.objects.filter(t_aka=main_id)
    t_foto = teams.objects.values('t_foto').get(pk=main_id)['t_foto']
    
    akas_list=get_akas(main_id)
    s_data = year + '-01-01'
    f_data = year + '-12-31'
    t_data_info = get_games_info (akas_list,s_data,f_data)
    
    Max_place,Min_place,g_count, \
    l_p,l_p_class,l_p_tuz, \
    l_p_tem,l_p_jub=get_team_year_results(t_data_info)

   
    l=[1,2,3,4,5,6,7,8,9,10]
    
    graph_tuz,graph_class,graph_summ = build_graph_team(t_id=team_id)
          

    context = {'team_id':team_id,'t_data_info': t_data_info, 't_names': t_names, 't_foto': t_foto, \
               't_data':t_data,'Max_place': Max_place,'Min_place' :Min_place, 'g_count':g_count, \
               'l': l,'l_p' : l_p,'l_p_class' : l_p_class,'l_p_tuz' : l_p_tuz, \
               'l_p_tem' :l_p_tem,'l_p_jub':l_p_jub , 'year' : year,\
               'graph_tuz':graph_tuz,'graph_class':graph_class,'graph_summ':graph_summ}
    
    return render(request, 'team_info.html', context)



def game_info (request):
    
    game_id = request.GET['game_id']
    g_data_info = gmdata.objects.filter(gd_game = game_id).order_by('gd_place')
    game_info =  games.objects.get(pk=game_id)
    a = games.objects.get(pk=game_id).g_sets
    year = games.objects.values('g_date').get(pk=game_id)['g_date'].year
    
    tours=[]
    for i in range(1, a+1): 
       tours.append(i)

    tuz_r=get_top10_teams_rating(type_of_data='tuz',game_date=game_info.g_date)
    summ_r=get_top10_teams_rating(type_of_data='summ',game_date=game_info.g_date)
    class_r=get_top10_teams_rating(type_of_data='class',game_date=game_info.g_date)


    if request.user.is_authenticated:
       change_yes=1
    else: change_yes=0

    
    context = {'g_data_info': g_data_info, 'year' : year, 'game_info': game_info, 'tours' : tours, 'change_yes' : change_yes, \
                'summ_r' : summ_r, 'class_r' : class_r,'tuz_r' : tuz_r
              }
    
    return render (request, 'game_info.html', context )


def year_stat(request): 
    year = request.GET['year']
    s_data = year + '-01-01'
    f_data = year + '-12-31'
    g_count = get_games_count(s_data,f_data)
    #game1 = games.objects.all() 
    game1 = get_games_all_in_range(s_data,f_data)
    t_data = get_all_teams()     

    
    place_data_a_1=get_place(1,type1=[1,2,3,4,5],data_start = s_data, data_finish = f_data) 
    place_data_a_2=get_place(2,type1=[1,2,3,4,5],data_start = s_data, data_finish = f_data) 
    place_data_a_3=get_place(3,type1=[1,2,3,4,5],data_start = s_data, data_finish = f_data) 
    place_data_cl_1=get_place(1,type1=[1,5],data_start = s_data, data_finish = f_data) 
    place_data_cl_2=get_place(2,type1=[1,5],data_start = s_data, data_finish = f_data) 
    place_data_cl_3=get_place(3,type1=[1,5],data_start = s_data, data_finish = f_data) 
    place_data_tz_1=get_place(1,type1=[2],data_start = s_data, data_finish = f_data) 
    place_data_tz_2=get_place(2,type1=[2],data_start = s_data, data_finish = f_data) 
    place_data_tz_3=get_place(3,type1=[2],data_start = s_data, data_finish = f_data)
    place_data_tem_1=get_place(1,type1=[3],data_start = s_data, data_finish = f_data)  
    place_data_tem_2=get_place(2,type1=[3],data_start = s_data, data_finish = f_data)  
    place_data_tem_3=get_place(3,type1=[3],data_start = s_data, data_finish = f_data)  
     

    context = {'game1': game1, 'g_count' : g_count, 't_data' : t_data, 'year' : year, \
               'place_data_a_1' : place_data_a_1, 'place_data_a_2' : place_data_a_2,'place_data_a_3' : place_data_a_3,\
               'place_data_cl_1' : place_data_cl_1, 'place_data_cl_2' : place_data_cl_2,'place_data_cl_3' : place_data_cl_3,\
               'place_data_tz_1' : place_data_tz_1, 'place_data_tz_2' : place_data_tz_2,'place_data_tz_3' : place_data_tz_3,\
               'place_data_tem_1' : place_data_tem_1, 'place_data_tem_2' : place_data_tem_2,'place_data_tem_3' : place_data_tem_3 }
 
    
    return render(request, 'year_stat.html', context)   

def compare (request):

   compare_yes=0
   context1={}
   context2={}
   context3={}
   t_data = get_all_teams() 

   if request.method == 'GET' and request.GET.get('team_id1') and request.GET.get('team_id2'):
      compare_yes=1
      team_id1 = request.GET['team_id1']
      team_id2 = request.GET['team_id2']
      try:
        year = request.GET['year']
      except:
        year='2025'

      
      main_id1 = teams.objects.values('t_aka_id').get(pk=team_id1)['t_aka_id']
      t_names1 = teams.objects.filter(t_aka=main_id1)
      
      akas_list1=get_akas(main_id1)
      s_data = year + '-01-01'
      f_data = year + '-12-31'
      t_data_info1 = get_games_info (akas_list1,s_data,f_data)
      Max_place1,Min_place1,g_count1, \
      l_p1,l_p_class1,l_p_tuz1, \
      l_p_tem1,l_p_jub1=get_team_year_results(t_data_info1)

      main_id2 = teams.objects.values('t_aka_id').get(pk=team_id2)['t_aka_id']
      t_names2 = teams.objects.filter(t_aka=main_id2)
      
      akas_list2=get_akas(main_id2)
      s_data = year + '-01-01'
      f_data = year + '-12-31'
      t_data_info2 = get_games_info (akas_list2,s_data,f_data)
      Max_place2,Min_place2,g_count2, \
      l_p2,l_p_class2,l_p_tuz2, \
      l_p_tem2,l_p_jub2=get_team_year_results(t_data_info2)

      context1 = {'t_data_info1': t_data_info1, 't_names1': t_names1, \
               'Max_place1': Max_place1,'Min_place1' :Min_place1, 'g_count1':g_count1, \
               'l_p1' : l_p1,'l_p_class1' : l_p_class1,'l_p_tuz1' : l_p_tuz1, \
               'l_p_tem1' :l_p_tem1,'l_p_jub1':l_p_jub1}  
      context2 = {'t_data_info2': t_data_info2, 't_names2': t_names2, \
               'Max_place2': Max_place2,'Min_place2' :Min_place2, 'g_count2':g_count2, \
               'l_p2' : l_p2,'l_p_class2' : l_p_class2,'l_p_tuz2' : l_p_tuz2, \
               'l_p_tem2' :l_p_tem2,'l_p_jub2':l_p_jub2} 
      
      graph_tuz,graph_class,graph_summ = build_graph_team_compare(t_id1=team_id1,t_id2=team_id2)

      context3 = {'graph_tuz':graph_tuz,'graph_class':graph_class,'graph_summ':graph_summ}
               
   compared_teams=[1,2]

   context={'compare_yes' : compare_yes, 't_data' :t_data, 'compared_teams' : compared_teams } | context1  | context2 | context3

   return render(request, 'compare.html', context )



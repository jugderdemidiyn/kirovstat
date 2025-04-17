from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import ModelForm,forms
import datetime
from itertools import islice

from . models import game_type, games, teams, gmdata, weekr
from . defs_1 import * 
from . defs_2 import * 



class AddGameData(ModelForm):
    class Meta:
        model = gmdata
        fields = ['gd_game','gd_team','gd_place',]

def add_game (request):
    
    if request.method == 'POST' and request.FILES['file']:

        f_name=request.FILES['file']

        dl=parse_excel_to_dict_list(f_name)
       

        global game_id_for_add
        global cheked_list
        cheked_list=[]

        cheked_g_name={}
        game_id_for_add=0
        
        g_name,g_id,tours=check_game_name(list(dl[0])[0])
                
        cheked_g_name [g_name]= g_id
        cheked_g_name ['Туров']= tours
                
        game_id_for_add=g_id

        for i in dl:
         
            j=list(i.values())
            cheked_list_line={}
            
            a_name,a_id = check_team_name (j[0])
            
            cheked_list_line['dl_name']=j[0]
            cheked_list_line['ch_name']=a_name
            cheked_list_line['ch_id']=a_id
            
            for t in range(1,tours+1):
                  tour_place=t+1
                  cheked_list_line[t]=j[tour_place]
            for t1 in range(tours+1,11):
                cheked_list_line[t1]=0
            cheked_list_line['place']=j[-1] 
            cheked_list_line['summ']=j[-2] 
            cheked_list.append(cheked_list_line)

            

        context1 = { 'dl' : cheked_list , 'gl' : cheked_g_name }
        #print (cheked_g_name)
        return render (request, 'load_game.html', context1)
    
    if request.method == 'GET' and request.GET.get('add_yes'):
        
        #print(cheked_list)

        for i in cheked_list:
            ch_id=i['ch_id']
            if ch_id==0:
                ch_id=208
            new_data=gmdata(
            gd_game=games.objects.get(pk=game_id_for_add),
            gd_team=teams.objects.get(pk=ch_id),
            gd_set1=i[1], 
            gd_set2=i[2],
            gd_set3=i[3], 
            gd_set4=i[4], 
            gd_set5=i[5], 
            gd_set6=i[6], 
            gd_set7=i[7], 
            gd_set8=i[8], 
            gd_set9=i[9], 
            gd_set10=i[10], 
            gd_summ=i['summ'], 
            gd_place = i['place']
            )
            new_data.save()
        redir_addr = '/kirovstat/game_info/?game_id='+ str(game_id_for_add)

        game_id_for_add=0
        cheked_list=[]

        return redirect(redir_addr)


    return render(request, 'add_game_file.html')

 


def add_res_to_stat(request):

    # закидывем номера и даты недель
    if request.method == 'GET' and request.GET.get('add_weeks'):
    
        date_start=datetime.datetime(2015,12,28)
        date_end = datetime.datetime(2025,12,31)
        date=date_start
        
        while date<date_end:
    
            end_week = date + datetime.timedelta(days=6)  
            
            if weekr.objects.values('week_start').get(pk=1)['week_start']:
                print('Уже есть')
                break
            weeks_2_add = weekr(
                week_start=date,
                week_end=end_week
                )
            
            date= date + datetime.timedelta(days=7)
        
        context = { 'res': " Занесли недели, позырь в PGAdmin" }
  


        return render(request, 'statstat.html', context)        
    
    # добавление заработанных очков на неделе

    if request.method == 'GET' and request.GET.get('count_weeks'):

        weeks = weekr.objects.all()
        
        for i in weeks:
    
            team_point_week_summ={}
            team_point_week_tuz={}
            team_point_week_class={}

            for j in get_games_in_range (str(i.week_start),str(i.week_end)):
                
                g_data_info = gmdata.objects.filter(gd_game = j).order_by('gd_place')
                game_curr_type = games.objects.values('g_type').get(pk=j)['g_type']
                
                team_point_week={}

                for place in range(1,11):
                    
                    for tt in g_data_info:
                        if tt.gd_place == place:
                        
                            if team_point_week.get(tt.gd_team.id):
                               team_point_week[tt.gd_team.id]=team_point_week[tt.gd_team.id]+COUNT_POINT[place]
                            else:
                               team_point_week [tt.gd_team.id]=COUNT_POINT[place]
                               
                if not game_curr_type == 4: 
                    if game_curr_type == 2:
                        team_point_week_tuz=merge_dicts(team_point_week_tuz, team_point_week)
                        
                    elif game_curr_type == 1 or game_curr_type == 5:
                        team_point_week_class=merge_dicts(team_point_week_class, team_point_week)

                    team_point_week_summ=merge_dicts(team_point_week_summ, team_point_week)

            #print('summ ', team_point_week_summ,' tuz', team_point_week_tuz, 'class ', team_point_week_tuz,)               

            new_data=i
        
            i.week_points_tuz = team_point_week_tuz
            i.week_points_class = team_point_week_class
            i.week_points_summ = team_point_week_summ
            
            new_data.save()
                    
        
               
        context = { 'res': " Занесли данные по неделям, позырь в PGAdmin" }
       
        return render(request, 'statstat.html', context)

    # подсчет и занесение рейтинга за последние 26 недель

    if request.method == 'GET' and request.GET.get('rating_4_id'):

        weeks = weekr.objects.filter(id__gte=28)
        
        for i in weeks:
           
            t,c,s = count_points_4_date(r_data=i.week_end,weeks=26)
            #print (dict(list(islice(c.items(), 0, 10))))

            new_data=i

            i.week_rating_tuz = dict(list(islice(t.items(), 0, 10)))
            i.week_rating_class = dict(list(islice(c.items(), 0, 10)))
            i.week_rating_summ = dict(list(islice(s.items(), 0, 10)))
        
            new_data.save()

        context = { 'res': " ННННННННН " }

        return render(request, 'statstat.html', context)

    context = { 'res': " В целом нихуя" }
    return render(request, 'statstat.html',context)



def test1 (request):
    
    graph1 = build_graph_1()
        
    context = {'graph1' : graph1 }
    
    return render (request, 'test1.html', context )
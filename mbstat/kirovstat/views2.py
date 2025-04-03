from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from django.forms import ModelForm,forms


from . models import game_type, games, teams, gmdata
from . defs_1 import * 


class AddGameData(ModelForm):
    class Meta:
        model = gmdata
        fields = ['gd_game','gd_team','gd_place',]


#  нахождение максимально похожей команды по имени
def check_team_name(t_name):

    t_names = teams.objects.values_list('t_name','id')
    
    a=20
    a_name='нет команды'
    #a_id=0
    name_len_diff=40
    for i in t_names:
        
        a1=len(set(t_name.lower())-set (i[0].lower()))
        name_len_diff1 = len(t_name)-len(i[0])
       
        if a1<a or (a1==a and abs(name_len_diff1)<name_len_diff):
            a=a1
            a_name=i[0]
            a_id=i[1]
            name_len_diff=abs(name_len_diff1)
    
    if a>2 or name_len_diff>15:
        a_name='нет команды'
        a_id=0

    return (a_name,a_id)

#  нахождение максимально похожей игры по имени

def check_game_name(g_name):
    
    g_names = games.objects.values_list('g_name','id','g_sets')
    a=20
    a_name='нет игры'
    name_len_diff=10
    for i in g_names:
        
        a1=len(set(g_name.lower())- set(i[0].lower()))
        name_len_diff1 = len(g_name)-len(i[0])
        
        if a1<a or (a1==a and abs(name_len_diff1)<name_len_diff):
            a=a1
            a_name=i[0]
            g_id=i[1]
            g_sets=i[2]
            name_len_diff=abs(name_len_diff1)
    
    if a>2 or name_len_diff>5:
        g_name='нет игры'
        g_id=0
    return (a_name, g_id, g_sets)

def parse_excel_to_dict_list(filepath: str, sheet_name='Sheet1'):
    # Загружаем Excel файл в DataFrame
    df = pd.read_excel(filepath)
                       #,sheet_name=sheet_name)

    # Преобразуем DataFrame в список словарей
    dict_list = df.to_dict(orient='records')

    return dict_list



def add_game (request):
    
    if request.method == 'POST' and request.FILES['file']:

        f_name=request.FILES['file']

        dl=parse_excel_to_dict_list(f_name)
              
        global cheked_list
        cheked_list=[]

        cheked_g_name={}
        
        g_name,g_id,tours=check_game_name(list(dl[0])[0])
        print(check_game_name(list(dl[0])[0]))
        
        cheked_g_name [g_name]= g_id
        cheked_g_name ['Туров']= tours
        
        global game_id_for_add
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
                ch_id=174
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
        return redirect(redir_addr)


    return render(request, 'add_game_file.html')
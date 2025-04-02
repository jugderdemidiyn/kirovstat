from django.shortcuts import render
from django.http import HttpResponse 
import pandas as pd
from django.forms import ModelForm


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

#  нахождение максимально похожей команды по имени

def check_game_name(g_name):
    
    g_names = games.objects.values_list('g_name','id')
    a=20
    a_name='нет игры'
        
    name_len_diff=10
    for i in g_names:
        
        a1=len(set(g_name.lower())- set(i[0].lower()))
        name_len_diff1 = len(g_name)-len(i[0])
        # print(g_name.lower(), i[0].lower())
        if a1<a or (a1==a and abs(name_len_diff1)<name_len_diff):
            a=a1
            a_name=i[0]
            g_id=i[1]
            name_len_diff=abs(name_len_diff1)
    
    if a>2 or name_len_diff>15:
        g_name='нет игры'
        g_id=0
    return (g_name, g_id)

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
        
        tours = 7
        
        global cheked_list
        cheked_list=[]
        cheked_g_name={}

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
            cheked_list_line['place']=j[-1] 
            cheked_list_line['summ']=j[-2] 
            cheked_list.append(cheked_list_line)

            g_name,g_id=check_game_name(list(i.keys())[0])
            cheked_g_name [g_name]= g_id
            global game_id_for_add
            game_id_for_add=g_id

        context1 = { 'dl' : cheked_list , 'gl' : cheked_g_name }
        #print (cheked_g_name)
        return render (request, 'load_game.html', context1)
    
    if request.method == 'GET' and request.GET.get('add_yes'):
        
        print(cheked_list)

        for i in cheked_list:
            new_data=gmdata(
            gd_game=game_id_for_add,
            gd_team=i['ch_id'],
            gd_set1=i[1], 
            gd_set2=i[2],
            gd_set3=i[3], 
            gd_set4=i[4], 
            gd_set5=i[5], 
            gd_set6=i[6], 
            gd_set7=i[7], 
            gd_summ=i['summ'], 
            gd_place = i['place']
            )
            new_data.save()

        return HttpResponse (html)


    return render(request, 'add_game_file.html')
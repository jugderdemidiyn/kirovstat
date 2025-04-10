from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import ModelForm,forms
import datetime


from . models import game_type, games, teams, gmdata, weekr
from . defs_1 import * 


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
        
        # print(check_game_name(list(dl[0])[0]))
        
        
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
            #weeks_2_add.save()
            #print (weeks_2_add)
            date= date + datetime.timedelta(days=7)
        
        context = { 'res': " Занесли недели, позырь в PGAdmin" }

        return render(request, 'statstat.html', context)        
   



    context = { 'res': " В целом нихуя" }
    return render(request, 'statstat.html',context)
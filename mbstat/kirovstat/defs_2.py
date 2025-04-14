from . models import game_type, games, teams, gmdata, weekr
from datetime import date
import collections as coll
from operator import itemgetter
import pandas as pd
import datetime


#id игр  -   1 классика 2 туц 3 тематика 4 юбилей 5 классика тематика



def get_week_id (rating_data):
    if rating_data.weekday() == 6:
       rating_week_data = rating_data
    else:
       td = 6 - int(rating_data.weekday())
       rating_week_data= rating_data + datetime.timedelta(days=td)

    week_id = weekr.objects.values('id').get(week_end=rating_week_data)['id']
    return (week_id)    

# сумма рейтинга по команде, дате  и количеству недель

def get_rating_points(t_id=0, rating_data=date.today(), weeks=10):

    week_id = get_week_id(rating_data)
    week_id_start = week_id - weeks
    
    week_data = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id).values_list('week_points_tuz','week_points_class','week_points_summ')
    
    tuz_points=0
    class_points=0
    summ_points=0

    for i in week_data:
        i
        if eval(i[0]).get(t_id): 
           # print (type(eval(i[0])))
           tuz_points = tuz_points + eval(i[0])[t_id]
        if eval(i[1]).get(t_id): 
           class_points = class_points + eval(i[1])[t_id]
        if eval(i[2]).get(t_id):  
           summ_points = summ_points + eval(i[2])[t_id]
    return (tuz_points,class_points,summ_points)
    #print (tuz_points,' ', class_points, ' ', summ_points)


#  получение списка с сумой рейтинговых баллов для всех команд 
#  на дату и количесто недель 
#  возвращает три списка по туц, классике и сумме

def count_points_4_date(r_data=date.today(), weeks=40):
   
    tuz_rat={}
    class_rat={}
    summ_rat={}

    for i in teams.objects.values('id','t_name'):
        #print (i['t_name'])
        t,c,s=get_rating_points(t_id=i['id'],rating_data=r_data,weeks=weeks)

      #print (t,' ',c,' ',s)
        if not t == 0:
           if tuz_rat.get(i['id']):
             tuz_rat[i['id']] = tuz_rat[i['id']] + t
           else: tuz_rat[i['id']]=t
        if not c == 0:
            if class_rat.get(i['id']):
              class_rat[i['id']] = class_rat[i['id']]+c 
            else: class_rat[i['id']]=c
        if not s == 0:
            if summ_rat.get(i['id']):
              summ_rat[i['id']] = summ_rat[i['id']]+s 
            else: summ_rat[i['id']]=s

    
    tuz_rat_sort=dict(sorted(tuz_rat.items(), key=itemgetter(-1), reverse = True))
    class_rat_sort=dict(sorted(class_rat.items(), key=itemgetter(-1), reverse = True))
    summ_rat_sort=dict(sorted(summ_rat.items(), key=itemgetter(-1), reverse = True))

    return (tuz_rat_sort,class_rat_sort,summ_rat_sort)


def get_rating (date=date.today(), weeks=3):

    week_id_end = get_week_id (date)
    week_id_start = week_id_end - weeks

    rating_data = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id_end).values('week_end','week_rating_tuz','week_rating_class','week_rating_summ')
    print (rating_data)
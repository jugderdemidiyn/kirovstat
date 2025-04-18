from . models import game_type, games, teams, gmdata, weekr
from datetime import date
import collections as coll
from operator import itemgetter
import pandas as pd
import datetime
import matplotlib 
import matplotlib.pyplot as plt
import io
import urllib, base64
from . defs_1 import *
from . views import *
matplotlib.use('agg')



#id игр  -   1 классика 2 туц 3 тематика 4 юбилей 5 классика тематика



def get_week_id (rating_data):
    
    if rating_data.weekday() == 6:
       rating_week_data = rating_data
    else:
       td = 6 - int(rating_data.weekday())
       rating_week_data= rating_data + datetime.timedelta(days=td)

    week_id = weekr.objects.values('id').get(week_end=rating_week_data)['id']
    return (week_id)    

# сумма рейтинга по команде, дате и количеству недель

def get_rating_points(t_id=0, rating_data=date.today(), weeks=10):

    week_id = get_week_id(rating_data)
    week_id_start = week_id - weeks
    
    week_data = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id).values_list('week_points_tuz','week_points_class','week_points_summ')
    
    tuz_points=0
    class_points=0
    summ_points=0

    for i in week_data:
        
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


def get_rating (date=date.today(), weeks=4):
    
    rating_data=date
    week_id_end = get_week_id (rating_data)
    week_id_start = week_id_end - weeks

    rating_data_tuz = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id_end).values('week_end','week_rating_tuz')
    rating_data_class = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id_end).values('week_end','week_rating_class')
    rating_data_summ = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id_end).values('week_end','week_rating_summ')
    # print (rating_data_class)

    return(rating_data_tuz,rating_data_class,rating_data_summ)


# сумма рейтига для команды(с ака) за кол-во недель
def get_rating_for_team (rt_data=date.today(), weeks=20,team_id=0):

    main_id = teams.objects.values('t_aka_id').get(pk=team_id)['t_aka_id']
    main_name = teams.objects.values('t_name').get(pk=main_id)['t_name']
    print(main_name)
    aka_l=get_akas(main_id)
    
    rating_data=rt_data
    
    week_id_end = get_week_id (rating_data)
    week_id_start = week_id_end - weeks

    tuz_team_points=0
    class_team_points=0
    summ_team_points=0
    tuz_graph=[]
    class_graph=[]
    summ_graph=[]

    rating_data = weekr.objects.filter(id__gte=week_id_start, id__lte=week_id_end).values_list('week_points_tuz','week_points_class','week_points_summ','week_end')
    
    for i in rating_data:
      
      for j in aka_l:
          
          if eval(i[0]).get(j): 
           tuz_team_points = tuz_team_points + eval(i[0])[j]
          if eval(i[1]).get(j): 
           class_team_points = class_team_points + eval(i[1])[j]
          if eval(i[2]).get(j): 
           summ_team_points = summ_team_points + eval(i[2])[j]
      tuz_graph.append((str(i[3]),tuz_team_points))
      class_graph.append((str(i[3]),class_team_points))
      summ_graph.append((str(i[3]),summ_team_points))
         
    #print(summ_graph)
        
    return(tuz_graph,class_graph,summ_graph,main_name)

def build_graph_1():
   
  rating_tuz,rating_class,rating_summ =get_rating()
  #print(rating_tuz)
  data_tuz=[]
  for i in rating_tuz:
    week_end=str(i['week_end'])
    dict_data1=eval(i['week_rating_tuz'])
    #print (type(dict_data1))
    for key,value in dict_data1.items():
      team_name = teams.objects.values('t_name').get(pk=int(key))['t_name']
      a=(week_end,team_name,value)
      data_tuz.append(a)
    
  df=pd.DataFrame(data_tuz)
  df2= df.set_axis({'week_end','points','team_name'},axis=1)
  
  print (df2)
 
  pd.plotting.parallel_coordinates(df2,'team_name ')
  buffer = io.BytesIO()
  #plt.savefig(buffer, format='png')
  #plt.savefig('test1.png', format='png')
  image_data = base64.b64encode(buffer.read()).decode()
  #plt.close()

  return (image_data)    
  

def build_graph_team(date=date.today(), weeks=60, t_id=1):

  
  
  rating_tuz,rating_class,rating_summ,main_name=get_rating_for_team(rt_data=date.today(),weeks=60,team_id=t_id) 
  
  plt.style.use(["fast"])
 
  pd.DataFrame(rating_tuz).plot(x=0,y=1,label=main_name)
  plt.ylabel('Рейтинг за Туц-Туц')
  plt.xlabel('Неделя')
  plt.title('Музыкальный рейтинг')
  plt.legend(loc="upper left", fontsize=10, facecolor="lightgray", edgecolor="black")
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  graph_tuz = base64.b64encode(buffer.getvalue()).decode()
  plt.close()

  pd.DataFrame(rating_class).plot(x=0,y=1,label=main_name)
  plt.ylabel('Рейтинг за Классику')
  plt.xlabel('Неделя')
  plt.title('Классические игры')
  plt.legend(loc="upper left", fontsize=10, facecolor="lightgray", edgecolor="black")
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  graph_class = base64.b64encode(buffer.getvalue()).decode()
  plt.close()

  
  pd.DataFrame(rating_summ).plot(x=0,y=1,label=main_name)
  plt.ylabel('Суммарный рейтинг')
  plt.xlabel('Неделя')
  plt.title('Общяя статитика')
  plt.legend(loc="upper left", fontsize=10, facecolor="lightgray", edgecolor="black")
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  graph_summ = base64.b64encode(buffer.getvalue()).decode()
  plt.close()
    
  return (graph_tuz,graph_class,graph_summ) 
  
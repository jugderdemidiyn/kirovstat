from . models import game_type, games, teams, gmdata, weekr
from datetime import date
import collections as coll
from operator import itemgetter
import pandas as pd
import datetime
import matplotlib 
import matplotlib.pyplot as plt

import numpy as np
import io
import urllib, base64
from . defs_1 import *
from . defs_2 import *
from . views import *

# 10 команд по рейтингу на дату и тип (tuz,class,summ)
# возвращает словарь { id команды : [имя рейтинг]}
def get_top10_teams_rating(game_date=date.today(),type_of_data='summ'):

  week_id=get_week_id (game_date)  
  if type_of_data == 'tuz':
    dict_of_rating=weekr.objects.values('week_rating_tuz').get(pk=week_id)['week_rating_tuz'] 
  elif type_of_data == 'class':
    dict_of_rating=weekr.objects.values('week_rating_class').get(pk=week_id)['week_rating_class']  
  else:
    dict_of_rating=weekr.objects.values('week_rating_summ').get(pk=week_id)['week_rating_summ'] 
  
  dict_of_rating_sorted=dict(sorted(eval(dict_of_rating).items(), key=itemgetter(-1), reverse = True))
  top10_ids=list(dict(itertools.islice(dict_of_rating_sorted.items(), 0,10)).keys())
  top10={}
  l=[]
  for i in top10_ids:
    
    try:
       l.append(teams.objects.values('t_name').get(pk=i)['t_name'])
    except:
       l.append('Чёт не найдено')
    l.append(eval(dict_of_rating)[i])
    top10[i]=l
    l=[] 

  return (top10)
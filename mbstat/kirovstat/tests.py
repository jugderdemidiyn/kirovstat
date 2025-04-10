import sys
from django.test import TestCase
from django.db.models import Avg, Max, Min, Sum
#from models import game_type, games, teams, gmdata, weekr
import datetime

# from . defs_1 import 

# print(sys.path)

#years=(2016,2017,2018,2019,2020,2021,2022,2023,2024,2025)
f_sunday =((2016, 1, 3),(2017, 1, 1),(2018, 1, 7),(2019, 1, 6),(2020, 1, 5),(2021, 1, 3),(2022, 1, 2),(2023, 1, 1),(2024, 1, 7),(2025, 1, 5))

#date=datetime.datetime(2016, 1, 3)
#for t in f_sunday:
    
#date=datetime.datetime(t[0],t[1],t[2])
date_start=datetime.datetime(2015, 12, 28)
    #print (date)
    #print (date.weekday())
    #for i in range (1,53):
    #    print(str(i),'-',date.year, ' ', date ) 
    #    date= date + datetime.timedelta(days=7)
    #    print(date.strftime("%V"))
date_end = datetime.datetime(2025,12,31)
date=date_start
while date<date_end:
    print ('monday',date,' ', date.weekday())  
    end_week =date + datetime.timedelta(days=6)  
    print ('sunday',end_week,' ',end_week.weekday()) 
    
    date= date + datetime.timedelta(days=7)


    #print (date.weekday())
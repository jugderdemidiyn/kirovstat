from django.shortcuts import render
from django.http import HttpResponse 
import pandas as pd

from . models import game_type, games, teams, gmdata
from . defs_1 import * 


def parse_excel_to_dict_list(filepath: str, sheet_name='Sheet1'):
    # Загружаем Excel файл в DataFrame
    df = pd.read_excel(filepath)
                       #,sheet_name=sheet_name)

    # Преобразуем DataFrame в список словарей
    dict_list = df.to_dict(orient='records')

    return dict_list



def add_game (request):
    
    
    f_name='./media/Классика 04.12.24.xlsx'

    dl=parse_excel_to_dict_list(f_name)
    #print(dl)
    context = {'dl' : dl }
    
    return render (request, 'load_game.html', context )
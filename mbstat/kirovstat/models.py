from django.db import models


class game_type(models.Model):
    type_name=models.CharField(verbose_name='Вид игры',max_length=50)

    class Meta: 
       verbose_name_plural = 'Типы игры' 
       verbose_name = 'Тип игры' 
       ordering = ['type_name'] 


    def __str__(self):
        return self.type_name

class teams (models.Model):
    t_name = models.CharField(verbose_name='Название команды',max_length=50)
    t_aka = models.ForeignKey('self',blank=True,null=True,on_delete=models.SET_NULL)
    t_page = models.URLField(default='http://rudagames.ru')
    t_foto = models.CharField(verbose_name='Фото команды',default='.foto.jpg',max_length=50)
    time_data = models.DateTimeField(auto_now=True, db_index=True, verbose_name='создано') 
    
    class Meta: 
       verbose_name_plural = 'Команды' 
       verbose_name = 'Команда' 
       ordering = ['t_name'] 

    def __str__(self):
        return self.t_name
    
class games (models.Model):
    g_name = models.CharField(default="Название игры", max_length=100)
    g_type = models.ForeignKey(game_type,null=True, on_delete=models.SET_NULL)
    g_date = models.DateField(verbose_name='Дата игры')
    g_sets = models.IntegerField(verbose_name='Количесто туров',default=5)
    g_url = models.URLField(verbose_name='Ссылка на игра в ВК',default="https://vk.com/mzgb_kir", max_length=200)
    time_data = models.DateTimeField(auto_now=True,db_index=True, verbose_name='создано') 
    g_teams = models.IntegerField(verbose_name='Количество команда',null=True, default = 1)

    class Meta: 
       verbose_name_plural = 'Игра' 
       verbose_name = 'Игры' 
       ordering = ['-g_date'] 

    def __str__(self):
        return self.g_name 
    
class gmdata (models.Model):
    gd_game = models.ForeignKey(games, verbose_name='Игра',null=False, on_delete = models.CASCADE)
    gd_team = models.ForeignKey(teams, verbose_name='Команда',null=False, on_delete = models.CASCADE)
    gd_set1 = models.FloatField(verbose_name='Тур 1',max_length=5,default=300)
    gd_set2 = models.FloatField(verbose_name='Тур 2',max_length=5,default=300)
    gd_set3 = models.FloatField(verbose_name='Тур 3',max_length=5,default=300)
    gd_set4 = models.FloatField(verbose_name='Тур 4',max_length=5,default=300)
    gd_set5 = models.FloatField(verbose_name='Тур 5',max_length=5,default=300)
    gd_set6 = models.FloatField(verbose_name='Тур 6',max_length=5,default=300)
    gd_set7 = models.FloatField(verbose_name='Тур 7',max_length=5,default=300)
    gd_set8 = models.FloatField(verbose_name='Тур 8',max_length=5,default=300)
    gd_set9 = models.FloatField(verbose_name='Тур 9',max_length=5,default=300)
    gd_set10 = models.FloatField(verbose_name='Тур 10',max_length=5,default=300)
    gd_summ = models.FloatField(max_length=8, verbose_name='Сумма очков')
    gd_place = models.IntegerField(verbose_name='Место')
    time_data = models.DateTimeField(auto_now=True, db_index=True, verbose_name='создано') 

    class Meta: 
       verbose_name_plural = 'Данные' 
       verbose_name = 'Данные' 
       ordering = ['time_data'] 

    def __str__(self):
        self.ret1 = self.gd_game.g_name + " - " + str(self.gd_place) + " место "
        return self.ret1
           
class weekr (models.Model):
    
    
    week_start = models.DateField(verbose_name='Начало недели')
    week_end = models.DateField(verbose_name='Конец недели')
    week_points_tuz = models.CharField(verbose_name="Очки команд за музыкалку",max_length=500)
    week_points_class = models.CharField(verbose_name="Очки команд за классику",max_length=500)
    week_points_summ = models.CharField(verbose_name="Очки команд всего",max_length=500)
    week_rating_tuz = models.CharField(verbose_name="10 рейтинга за музыкалку",max_length=200)
    week_rating_class = models.CharField(verbose_name="10 рейтинга за классику",max_length=200)
    week_rating_summ = models.CharField(verbose_name="10 рейтинга всего",max_length=200)
    

    class Meta: 
       verbose_name_plural = 'Статистика по неделям' 
       verbose_name = 'Статистика' 
       ordering = ['week_start'] 
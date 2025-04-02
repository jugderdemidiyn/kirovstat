from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from . import models

admin.site.register(models.game_type)
admin.site.register(models.teams)
admin.site.register(models.games)
#admin.site.register(models.gmdata)



class gmdataResource(resources.ModelResource):
 
    

    gd_team = Field( 
    column_name = "gd_team",
    attribute = "gd_team",
    widget = ForeignKeyWidget(models.teams, field='t_name'))
    

    gd_game = Field(
        column_name = "gd_game",
        attribute = "gd_game",
        widget = ForeignKeyWidget(models.games,field='g_name')
    )
    


    class Meta:
        model = models.gmdata
        exclude = ('time_data' )

@admin.register(models.gmdata)
class gmdataAdmin(ImportExportModelAdmin):
    resource_classes = [gmdataResource]
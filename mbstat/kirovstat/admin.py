from django.contrib import admin


from . import models

admin.site.register(models.game_type)
admin.site.register(models.teams)
admin.site.register(models.games)
admin.site.register(models.gmdata)


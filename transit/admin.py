from django.contrib import admin
from transit.models import Bus, Line, LineStopLink, Stop

class BusAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','line','arrival_times',)

class LineAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LineStopLinkAdmin(admin.ModelAdmin):
    list_display = ('line', 'stop', 'index')

class StopAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Bus, BusAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(LineStopLink, LineStopLinkAdmin)
admin.site.register(Stop, StopAdmin)
from django.contrib import admin
from transit.models import Bus, Line, LineStopLink, Stop

class BusAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','line','arrival_times',)
    
    def queryset(self, request):
        qs = super(BusAdmin, self).queryset(request)
        return qs.order_by('line__name','arrival_times')

class LineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    def queryset(self, request):
        qs = super(LineAdmin, self).queryset(request)
        return qs.order_by('name')

class LineStopLinkAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','line', 'stop', 'index')
    
    def queryset(self, request):
        qs = super(LineStopLinkAdmin, self).queryset(request)
        return qs.order_by('line__name', 'index')

class StopAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    def queryset(self, request):
        qs = super(StopAdmin, self).queryset(request)
        return qs.order_by('name')

admin.site.register(Bus, BusAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(LineStopLink, LineStopLinkAdmin)
admin.site.register(Stop, StopAdmin)
from django.contrib import admin
from transit.models import Bus, Line, LineStopLink, Stop

admin.site.register(Bus)
admin.site.register(Line)
admin.site.register(LineStopLink)
admin.site.register(Stop)
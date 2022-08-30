from django.contrib import admin
from .models import Flowchart, Location

# Register your models here.


class FlowchartAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'primary', 'is_active')
    list_filter = ('name', 'location', 'primary', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'location', 'primary', 'is_active')}),
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'incident_number')
    list_filter = ('name', )
    fieldsets = (
        (None, {'fields': ('name', 'incident_number')}),
    )


admin.site.register(Flowchart, FlowchartAdmin)
admin.site.register(Location, LocationAdmin)

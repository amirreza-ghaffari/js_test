from django.contrib import admin
from .models import Flowchart

# Register your models here.


class FlowchartAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('name', 'location')
    fieldsets = (
        (None, {'fields': ('name', 'location')}),
    )


admin.site.register(Flowchart, FlowchartAdmin)

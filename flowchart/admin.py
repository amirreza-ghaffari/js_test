from django.contrib import admin
from .models import Flowchart, Location, ContingencyPlan


class FlowchartAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'primary', 'is_active', 'incident_counter')
    list_filter = ('name', 'location', 'primary', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'location', 'primary', 'is_active', 'incident_counter')}),
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    fieldsets = (
        (None, {'fields': ('name',)}),
    )


class ContingencyPlanAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Flowchart, FlowchartAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ContingencyPlan, ContingencyPlanAdmin)

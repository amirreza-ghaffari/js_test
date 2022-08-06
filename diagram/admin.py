from django.contrib import admin
from .models import Block, Transition
from department.models import Department

# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    list_display = ('label', 'approved', 'active', 'color')
    list_filter = ('label', 'approved', 'active', 'color')
    fieldsets = (
        (None, {'fields': ('label', 'approved', 'active', 'color')}),
    )


class TransitionAdmin(admin.ModelAdmin):
    list_display = ('label', 'start_block', 'end_block', 'active', 'flow_path')
    list_filter = ('label', 'start_block', 'end_block', 'active')
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'active')}),
    )


admin.site.register(Block)
admin.site.register(Transition, TransitionAdmin)

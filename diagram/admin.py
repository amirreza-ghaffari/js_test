from django.contrib import admin
from .models import Block, Transition, BlockGroup
from department.models import Department

# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    fields = ('label', 'approved', 'active', 'color', 'group', 'department', 'figure', 'description',
              'thickness', 'fill', 'loc_height', 'loc_length', 'user_groups')
    list_display = ('label', 'approved', 'active', 'last_modified')
    list_filter = ('label', 'approved', 'active')


class TransitionAdmin(admin.ModelAdmin):

    list_display = ('label', 'start_block', 'end_block', 'active', 'last_modified')
    list_filter = ('label', 'start_block', 'end_block', 'active')
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'active')}),
    )


admin.site.register(Block, BlockAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(BlockGroup)

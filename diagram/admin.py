from django.contrib import admin
from .models import Block, Transition, BlockGroup
from department.models import Department

# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    fields = ('label', 'is_approved', 'is_active', 'color', 'group', 'department', 'figure', 'description',
              'thickness', 'fill', 'loc_height', 'loc_length', 'user_groups', 'is_conditional')
    list_display = ('id', 'label', 'is_approved', 'is_active', 'last_modified',)
    list_filter = ('label', 'is_approved', 'is_active')

    ordering = ['-created_date']


class TransitionAdmin(admin.ModelAdmin):

    list_display = ('label', 'start_block', 'end_block', 'is_approved', 'is_active', 'last_modified')
    list_filter = ('is_approved', 'is_active')
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'is_active', 'is_approved')}),
    )
    ordering = ['-created_date']


admin.site.register(Block, BlockAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(BlockGroup)

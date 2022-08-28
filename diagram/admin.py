from django.contrib import admin
from .models import Block, Transition, BlockGroup, Comment

# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    fields = ('label', 'is_approved', 'is_active', 'color', 'group', 'flowchart', 'figure', 'description',
              'thickness', 'fill', 'loc_height', 'loc_length', 'user_groups', 'is_conditional')
    list_display = ('id', 'label', 'is_approved', 'is_active', 'last_modified',)
    list_filter = ('is_approved', 'is_active', 'flowchart')


class TransitionAdmin(admin.ModelAdmin):

    list_display = ('label', 'start_block', 'end_block', 'is_approved', 'is_active', 'last_modified', 'flowchart')
    list_filter = ('is_approved', 'is_active', 'flowchart')
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'is_active', 'is_approved', 'flowchart')}),
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('label', 'author', 'block')
    list_filter = ('author', 'block')
    fieldsets = (
        (None, {'fields': ('label', 'text', 'author', 'block')}),
    )


admin.site.register(Block, BlockAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(BlockGroup)
admin.site.register(Comment, CommentAdmin)


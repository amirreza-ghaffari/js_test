from django.contrib import admin
from .models import Block, Transition, BlockGroup, Comment

# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    fields = ('label', 'is_approved', 'is_pre_approved', 'is_active', 'is_conditional', 'color', 'group', 'flowchart', 'figure', 'description',
              'loc_height', 'loc_length', 'members')
    list_display = ('id', 'label', 'is_approved', 'is_pre_approved', 'is_active', 'last_modified',)
    list_filter = ('is_approved', 'is_active', 'flowchart')
    search_fields = ['label', 'flowchart__name']


class TransitionAdmin(admin.ModelAdmin):

    list_display = ('label', 'start_block', 'end_block', 'is_approved', 'is_active', 'last_modified', 'flowchart')
    list_filter = ('is_approved', 'is_active', 'flowchart')
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'is_active', 'is_approved', 'flowchart')}),
    )
    search_fields = ['start_block']
    autocomplete_fields = ['start_block']



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


from django.contrib import admin
from .models import Block, Transition, Comment
from django.contrib.admin import ModelAdmin, SimpleListFilter
from flowchart.models import Flowchart


class BlockAdmin(admin.ModelAdmin):
    fields = ('label', 'is_approved', 'is_pre_approved', 'is_active', 'is_conditional', 'color', 'flowchart',
              'figure', 'loc_height', 'loc_length', 'members')
    list_display = ('id', 'label', 'is_approved', 'is_pre_approved', 'is_active', 'last_modified')
    list_filter = ('is_approved', 'is_active', 'is_pre_approved', 'flowchart')
    search_fields = ['label', 'flowchart__name']


class FlowchartFilter(SimpleListFilter):
    title = "Flowchart"  # a label for our filter
    parameter_name = "flow"  # you can put anything here

    def lookups(self, request, model_admin):
        list_of_flows = []
        queryset = Flowchart.objects.all()
        for flow in queryset:
            list_of_flows.append(
                (str(flow.id), flow.__str__())
            )
        return sorted(list_of_flows, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_block__flowchart_id=self.value(), end_block__flowchart_id=self.value())
        return queryset


class TransitionAdmin(admin.ModelAdmin):

    list_display = ('label', 'start_block_label', 'end_block_label', 'is_approved', 'is_active', 'last_modified')
    list_filter = ('is_approved', 'is_active', FlowchartFilter)
    fieldsets = (
        (None, {'fields': ('label', 'start_block', 'end_block', 'is_active', 'is_approved')}),
    )
    search_fields = ['start_block', 'end_block']
    autocomplete_fields = ['start_block', 'end_block']

    def start_block_label(self, obj):
        return obj.start_block.label

    def end_block_label(self, obj):
        return obj.start_block.label


class CommentAdmin(admin.ModelAdmin):
    list_display = ('label', 'author', 'block')
    list_filter = ('author', 'block')
    fieldsets = (
        (None, {'fields': ('label', 'text', 'author', 'block')}),
    )


admin.site.register(Block, BlockAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(Comment, CommentAdmin)


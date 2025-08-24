from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    exclude = ('custom_id',)
    list_display = ('custom_id', 'name', 'type', 'parent_display')
    search_fields = ('name',)
    list_filter = ('type',)

    autocomplete_fields = ['parent', 'equivalents']
    list_select_related = ('parent',)

    filter_horizontal = ('equivalents',)

    ordering = ('type', 'name')

    def parent_display(self, obj):
        return obj.parent.name if obj.parent else "-"

    parent_display.short_description = 'Parent Unit'

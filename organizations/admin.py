from django.contrib import admin
from .models import Organization, OrganizationType
from people.models import Person, PersonPosition, Cabinet


class PersonPositionInline(admin.TabularInline):
    model = PersonPosition
    fields = ['person', 'title', 'start', 'end']
    extra = 0
    readonly_fields = ['person', 'title', 'start', 'end']
    can_delete = False
    show_change_link = True

@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def has_module_permission(self, request):
        return False  # hides it from sidebar
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    exclude = ('custom_id',)
    list_display = ('custom_id', 'name', 'type', 'parent_display')
    search_fields = ('name',)
    list_filter = ('type',)

    autocomplete_fields = ['type', 'parent', 'equivalents']
    list_select_related = ('parent',)

    filter_horizontal = ('equivalents',)

    ordering = ('type', 'name')
    inlines = [PersonPositionInline]
    readonly_fields = ('children_display',)

    def parent_display(self, obj):
        return obj.parent.name if obj.parent else "-"

    parent_display.short_description = 'Parent Unit'

    def children_display(self, obj):
        children = obj.children.all()
        if not children:
            return "—"
        return ", ".join([child.name for child in children])

    children_display.short_description = "Children"

from django.contrib import admin
from django.utils.html import format_html_join, format_html
from .models import Organization, OrganizationType
from people.models import Person, PersonPosition, Cabinet


class PersonPositionInline(admin.TabularInline):
    model = PersonPosition
    fields = ['person', 'title', 'start', 'end']
    extra = 0
    readonly_fields = ['person', 'title', 'start', 'end']
    can_delete = False
    show_change_link = True

class ChildOrganizationInline(admin.TabularInline):
    model = Organization
    fk_name = 'parent'
    extra = 1
    fields = ['name', 'type', 'level']

@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def has_module_permission(self, request):
        return False  # hides it from sidebar
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    exclude = ('custom_id',)
    list_display = ('custom_id', 'name_link', 'type', 'parent_link')
    search_fields = ('name',)
    list_filter = ('type',)

    autocomplete_fields = ['type', 'parent', 'equivalents',]
    list_select_related = ('parent',)

    filter_horizontal = ('equivalents',)

    ordering = ('type', 'name')
    inlines = [PersonPositionInline, ChildOrganizationInline]
    readonly_fields = ('children_display',)

    def name_link(self, obj):
        return format_html('<a href="{}">{}</a>', f"/admin/organizations/organization/{obj.id}/change/", obj.name)
    name_link.short_description = "Name"
    name_link.admin_order_field = "name"

    def parent_link(self, obj):
        if obj.parent:
            return format_html('<a href="{}">{}</a>', f"/admin/organizations/organization/{obj.parent.id}/change/", obj.parent.name)
        return "—"
    parent_link.short_description = "Parent Unit"
    parent_link.admin_order_field = "parent"

    def parent_display(self, obj):
        return obj.parent.name if obj.parent else "-"

    parent_display.short_description = 'Parent Unit'

    def children_display(self, obj):
        children = obj.children.all()
        if not children:
            return "—"
        return format_html_join(
            ", ",
            '<a href="/admin/organizations/organization/{}/change/">{}</a>',
            ((child.id, child.name) for child in children)
        )

    children_display.short_description = "Children"
    readonly_fields = ('children_display',)
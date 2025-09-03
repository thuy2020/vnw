from django.contrib import admin
from .models import Legislation, PersonLegislation, OrganizationLegislation
from django.utils.html import format_html, format_html_join
from django.urls import reverse

@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'law_number',
        'date_passed',
        'date_effective',
        'list_people',
        'list_organizations',
    ]
    search_fields = ['title', 'law_number']
    filter_horizontal = ['people_involved', 'organizations_involved']

    def list_people(self, obj):
        people = obj.people_involved.all()
        return format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            [
                (
                    reverse("admin:people_person_change", args=[p.id]),
                    p.name
                )
                for p in people
            ]
        )
    list_people.short_description = "People Involved"

    def list_organizations(self, obj):
        orgs = obj.organizations_involved.all()
        return format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            [
                (
                    reverse("admin:organizations_organization_change", args=[o.id]),
                    o.name
                )
                for o in orgs
            ]
        )
    list_organizations.short_description = "Organizations Involved"

@admin.register(PersonLegislation)
class PersonLegislationAdmin(admin.ModelAdmin):
    list_display = ['person_name', 'legislation_title', 'role']
    search_fields = ['person__name', 'legislation__title', 'role']
    list_filter = ['role']

    def person_name(self, obj):
        return obj.person.name
    person_name.short_description = "Person"

    def legislation_title(self, obj):
        return obj.legislation.title
    legislation_title.short_description = "Legislation"


@admin.register(OrganizationLegislation)
class OrganizationLegislationAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'legislation_title', 'role']
    search_fields = ['organization__name', 'legislation__title', 'role']
    list_filter = ['role']

    def organization_name(self, obj):
        return obj.organization.name
    organization_name.short_description = "Organization"

    def legislation_title(self, obj):
        return obj.legislation.title
    legislation_title.short_description = "Legislation"
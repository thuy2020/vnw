from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Event, PersonEvent, OrganizationEvent
from legislation.models import Legislation


@admin.register(PersonEvent)
class PersonEventAdmin(admin.ModelAdmin):
    list_display = ['person', 'event', 'role']
    search_fields = ['person__name', 'event__title', 'role']
    list_filter = ['role']

@admin.register(OrganizationEvent)
class OrganizationEventAdmin(admin.ModelAdmin):
    list_display = ['organization', 'event', 'role']
    search_fields = ['organization__name', 'event__title', 'role']
    list_filter = ['role']

class LegislationInline(admin.TabularInline):
    model = Event.legislations_involved.through
    extra = 0
    verbose_name = "Legislation Event"
    verbose_name_plural = "Legislation Events"
    autocomplete_fields = ['legislation']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'date', 'location', 'category',
        'list_people', 'list_organizations', 'list_legislations'
    ]
    search_fields = ['title', 'summary', 'location']
    filter_horizontal = ['legislations_involved']
    inlines = [LegislationInline]

    def list_people(self, obj):
        return ", ".join(p.name for p in obj.people_involved.all())
    list_people.short_description = "People Involved"

    def list_organizations(self, obj):
        return ", ".join(o.name for o in obj.organizations_involved.all())
    list_organizations.short_description = "Organizations Involved"

    def list_legislations(self, obj):
        return ", ".join(l.title for l in obj.legislations_involved.all())
    list_legislations.short_description = "Legislations Involved"
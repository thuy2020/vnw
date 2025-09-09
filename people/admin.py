from django.contrib import admin
from django.http import HttpResponse

from .models import PersonPosition, Person, Cabinet, PersonRelationship
from django.urls import reverse
from django.utils.html import format_html
import unicodedata
from django.db.models.functions import Lower
from django.core.serializers import serialize
import json


class PersonPositionInline(admin.TabularInline):
    model = PersonPosition
    extra = 0
    max_num = None
    autocomplete_fields = ["organization"]

class PersonRelationshipInline(admin.TabularInline):
    model = PersonRelationship
    fk_name = 'from_person'
    autocomplete_fields = ['to_person']
    extra = 1

class PersonRelationshipReverseInline(admin.TabularInline):
    model = PersonRelationship
    fk_name = 'to_person'
    autocomplete_fields = ['from_person']
    extra = 0
    verbose_name = "Related From"
    verbose_name_plural = "Related From"
    can_delete = False
    readonly_fields = ['from_person', 'relationship_type']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = ('custom_id',)
    list_display = ("custom_id", "name", "hometown_province","date_of_birth", "date_of_death",
                    "position")
    change_list_template = "admin/people/change_list.html"
    search_fields = (
        "custom_id",
        "name_ascii", "name",
        "hometown",
        "hometown_province",
        "position",
        "foreign_language",
        "political_theory",
        "education",
        "ethnicity",
    )

    filter_horizontal = ("cabinets",)
    fields = ("name", "hometown", "hometown_province", "date_of_birth", "date_of_death", "gender",
              "foreign_language", "political_theory", "education",
              "position_process", "cabinets")
    inlines = [PersonRelationshipInline, PersonRelationshipReverseInline, PersonPositionInline]

    def get_search_results(self, request, queryset, search_term):
        normalized_term = unicodedata.normalize('NFKD', search_term).encode('ASCII', 'ignore').decode('utf-8').lower()
        matching_ids = set()

        for field in self.search_fields:
            for obj in self.model.objects.all():
                value = getattr(obj, field, "")
                value_normalized = unicodedata.normalize('NFKD', str(value)).encode('ASCII', 'ignore').decode('utf-8').lower()
                if normalized_term in value_normalized:
                    matching_ids.add(obj.id)

        return queryset.filter(id__in=matching_ids), False

    actions = ['export_selected_people']
    def export_selected_people(self, request, queryset):
        data = []
        for person in queryset:
            person_dict = {
                "person": json.loads(serialize('json', [person]))[0],
                "hometown_province": person.hometown_province,
                "positions": json.loads(serialize('json', person.positions.all())),
                "relationships_from": json.loads(serialize('json', person.relationships_from.all())),
                "relationships_to": json.loads(serialize('json', person.relationships_to.all())),
                #"cabinets": json.loads(serialize('json', person.cabinets.all())),
            }
            data.append(person_dict)
        response = HttpResponse(json.dumps(data, indent=2), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=selected_people.json'
        return response

    export_selected_people.short_description = "Export selected people"

class CabinetMemberInline(admin.TabularInline):
    model = Person.cabinets.through
    extra = 1
    verbose_name = "Cabinet Member"
    verbose_name_plural = "Cabinet Members"
    fields = ("person", "person_link")
    readonly_fields = ("person_link",)

    def person_link(self, obj):
        url = reverse("admin:people_person_change", args=(obj.person.id,))
        return format_html('<a href="{}">{}</a>', url, obj.person.name)

    person_link.short_description = "Member"


class CabinetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [CabinetMemberInline]

    def get_search_results(self, request, queryset, search_term):
        normalized_term = unicodedata.normalize('NFKD', search_term).encode('ASCII', 'ignore').decode('utf-8').lower()
        qs = self.model.objects.none()
        for field in self.search_fields:
            annotated_field = f"normalized_{field}"
            qs |= self.model.objects.annotate(**{
                annotated_field: Lower(field)
            }).filter(**{
                f"{annotated_field}__icontains": normalized_term
            })
        return qs.distinct(), False


admin.site.register(Cabinet, CabinetAdmin)

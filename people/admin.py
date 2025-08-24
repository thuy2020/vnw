from django.contrib import admin
from .models import PersonPosition, Person, Cabinet
from django.urls import reverse
from django.utils.html import format_html
import unicodedata
from django.db.models.functions import Lower


class PersonPositionInline(admin.TabularInline):
    model = PersonPosition
    extra = 0
    max_num = None


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = ('custom_id',)
    list_display = ("custom_id", "name", "hometown", "date_of_birth", "date_of_death",
                    "position")
    search_fields = (
        "custom_id",
        "name",
        "hometown",
        "position",
        "foreign_language",
        "political_theory",
        "education",
        "ethnicity",
    )
    filter_horizontal = ("cabinets",)
    fields = ("name", "hometown", "date_of_birth", "date_of_death", "gender",
              "foreign_language", "political_theory", "education",
              "position_process", "cabinets")
    inlines = [PersonPositionInline]

    def get_search_results(self, request, queryset, search_term):
        normalized_term = unicodedata.normalize('NFKD', search_term).encode('ASCII', 'ignore').decode('utf-8').lower()
        matching_ids = set()

        for field in self.search_fields:
            try:
                for obj in self.model.objects.all():
                    value = getattr(obj, field, "")
                    value_normalized = unicodedata.normalize('NFKD', str(value)).encode('ASCII', 'ignore').decode('utf-8').lower()
                    if normalized_term in value_normalized:
                        matching_ids.add(obj.id)
            except Exception:
                continue

        return queryset.filter(id__in=matching_ids), False


class CabinetMemberInline(admin.TabularInline):
    model = Person.cabinets.through
    extra = 1
    verbose_name = "Cabinet Member"
    verbose_name_plural = "Cabinet Members"
    readonly_fields = ("person_link",)
    fields = ("person_link",)

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

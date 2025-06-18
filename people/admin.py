from django.contrib import admin
from .models import Person, PersonPosition

class PersonPositionInline(admin.TabularInline):
    model = PersonPosition
    extra = 0
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonPositionInline]
    list_display = ('name', 'cabinet', 'hometown')
    list_filter = ('cabinet',)  # ✅ This adds the dropdown filter
    search_fields = ('name', 'cabinet')  # ✅ allows typing cabinet name in search box

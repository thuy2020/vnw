from django.contrib import admin
from .models import OrganizationUnit

@admin.register(OrganizationUnit)
class OrganizationUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'parent')  # You can customize this
    search_fields = ('name',)
    list_filter = ('type',)
